#!/usr/bin/env python3
"""
SVG Translation Tool

This tool extracts multilingual text pairs from SVG files and applies translations
to other SVG files by inserting missing <text systemLanguage="XX"> blocks.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from lxml import etree
import shutil
import tempfile


def setup_logging(verbose=False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def normalize_text(text):
    """Normalize text by trimming whitespace and collapsing internal whitespace."""
    if not text:
        return ""
    # Trim leading/trailing whitespace
    text = text.strip()
    # Replace multiple internal whitespace with single space
    text = ' '.join(text.split())
    return text


def extract_text_from_node(node):
    """Extract text from a text node, handling tspan elements."""
    # Try to find tspan elements first
    tspans = node.xpath('./svg:tspan', namespaces={'svg': 'http://www.w3.org/2000/svg'})
    if tspans:
        # Return a list of text from each tspan element
        return [tspan.text.strip() if tspan.text else "" for tspan in tspans]
    # Fall back to direct text content
    return [node.text.strip()] if node.text else [""]


def extract(svg_file_path, output_file=None, case_insensitive=True):
    """
    Extract translations from an SVG file and save them as JSON.

    Args:
        svg_file_path: Path to the SVG file to extract translations from
        output_file: Path to save the JSON output (defaults to <svg_file_path>.json)
        case_insensitive: Whether to normalize case when matching strings

    Returns:
        Dictionary containing the extracted translations
    """
    logger = logging.getLogger(__name__)
    svg_file_path = Path(svg_file_path)

    if not svg_file_path.exists():
        logger.error(f"SVG file not found: {svg_file_path}")
        return None

    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f'{svg_file_path.name}.json'

    logger.info(f"Extracting translations from {svg_file_path}")

    # Parse SVG as XML
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(str(svg_file_path), parser)
    root = tree.getroot()

    # Find all switch elements
    switches = root.xpath('//svg:switch', namespaces={'svg': 'http://www.w3.org/2000/svg'})
    logger.info(f"Found {len(switches)} switch elements")

    translations = {}
    processed_switches = 0

    for switch in switches:
        # Find all text elements within this switch
        text_elements = switch.xpath('./svg:text', namespaces={'svg': 'http://www.w3.org/2000/svg'})

        if not text_elements:
            continue

        # Identify default text (no systemLanguage attribute)
        default_text = None
        default_node = None

        # Find translations
        switch_translations = {}

        for text_elem in text_elements:
            system_lang = text_elem.get('systemLanguage')
            text_contents = extract_text_from_node(text_elem)

            if not system_lang:
                # This is the default text
                default_texts = [normalize_text(text) for text in text_contents]
                if case_insensitive:
                    default_texts = [text.lower() for text in default_texts]
                default_node = text_elem
            else:
                # This is a translation
                normalized_contents = [normalize_text(text) for text in text_contents]
                if case_insensitive:
                    normalized_contents = [text.lower() for text in normalized_contents]
                switch_translations[system_lang] = normalized_contents

        # If we found both default text and translations, add to our data
        if default_texts and switch_translations:
            # Create a key from the first default text (we could use all texts but this is simpler)
            default_key = default_texts[0]

            if default_key not in translations:
                translations[default_key] = {
                    '_texts': default_texts,  # Store all default texts
                    '_translations': {}      # Store translations for each text
                }

            # Store translations for each language and each text
            for lang, translated_texts in switch_translations.items():
                translations[default_key]['_translations'][lang] = translated_texts

            processed_switches += 1
            logger.debug(f"Processed switch with default texts: {default_texts}")

    # Save translations to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)

    logger.info(f"Extracted translations for {processed_switches} switches")
    logger.info(f"Saved translations to {output_file}")

    # Count languages
    all_languages = set()
    for text_dict in translations.values():
        all_languages.update(text_dict.keys())

    logger.info(f"Found translations in {len(all_languages)} languages: {', '.join(sorted(all_languages))}")

    return translations


def generate_unique_id(base_id, lang, existing_ids):
    """Generate a unique ID by appending language code and numeric suffix if needed."""
    new_id = f"{base_id}-{lang}"

    # If the base ID with language is unique, use it
    if new_id not in existing_ids:
        return new_id

    # Otherwise, add numeric suffix until unique
    counter = 1
    while f"{new_id}-{counter}" in existing_ids:
        counter += 1

    return f"{new_id}-{counter}"


def inject(svg_file_path, mapping_files, output_dir=None, overwrite=False, dry_run=False, case_insensitive=True):
    """
    Inject translations into an SVG file based on mapping files.

    Args:
        svg_file_path: Path to the SVG file to inject translations into
        mapping_files: List of paths to JSON mapping files
        output_dir: Directory to save modified SVG files (defaults to same directory as input)
        overwrite: Whether to overwrite existing translations
        dry_run: If True, only report changes without writing files
        case_insensitive: Whether to normalize case when matching strings

    Returns:
        Dictionary with statistics about the injection process
    """
    logger = logging.getLogger(__name__)
    svg_file_path = Path(svg_file_path)

    if not svg_file_path.exists():
        logger.error(f"SVG file not found: {svg_file_path}")
        return None

    # Load all mapping files
    all_mappings = {}
    for mapping_file in mapping_files:
        mapping_file = Path(mapping_file)
        if not mapping_file.exists():
            logger.warning(f"Mapping file not found: {mapping_file}")
            continue

        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mappings = json.load(f)

            # Merge mappings
            for key, value in mappings.items():
                if key not in all_mappings:
                    all_mappings[key] = {}
                all_mappings[key].update(value)

            logger.info(f"Loaded mappings from {mapping_file}")
        except Exception as e:
            logger.error(f"Error loading mapping file {mapping_file}: {str(e)}")
            return None

    if not all_mappings:
        logger.error("No valid mappings found")
        return None

    logger.info(f"Injecting translations into {svg_file_path}")

    # Parse SVG as XML
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(str(svg_file_path), parser)
    root = tree.getroot()

    # Find all switch elements
    switches = root.xpath('//svg:switch', namespaces={'svg': 'http://www.w3.org/2000/svg'})
    logger.info(f"Found {len(switches)} switch elements")

    # Collect all existing IDs to ensure uniqueness
    existing_ids = set(root.xpath('//@id'))

    stats = {
        'processed_switches': 0,
        'inserted_translations': 0,
        'skipped_translations': 0,
        'updated_translations': 0
    }

    for switch in switches:
        # Find all text elements within this switch
        text_elements = switch.xpath('./svg:text', namespaces={'svg': 'http://www.w3.org/2000/svg'})

        if not text_elements:
            continue

        # Identify default text (no systemLanguage attribute)
        default_texts = None
        default_node = None

        for text_elem in text_elements:
            system_lang = text_elem.get('systemLanguage')
            if not system_lang:
                text_contents = extract_text_from_node(text_elem)
                default_texts = [normalize_text(text) for text in text_contents]

                if case_insensitive:
                    default_texts = [text.lower() for text in default_texts]

                default_node = text_elem
                break

        if not default_texts:
            continue

        # Find matching translation in the mappings
        translation_key = None
        translations_data = None

        # Try to find a match using the first text as key
        first_text = default_texts[0]
        if first_text in all_mappings:
            translation_key = first_text
            translations_data = all_mappings[first_text]

        # If not found, try to match by comparing all texts
        if not translation_key:
            for key, data in all_mappings.items():
                if '_texts' in data and data['_texts'] == default_texts:
                    translation_key = key
                    translations_data = data
                    break

        if not translation_key:
            continue

        # Get available translations for this text
        available_translations = translations_data.get('_translations', {})

        # Check which translations already exist
        existing_languages = set()
        for text_elem in text_elements:
            system_lang = text_elem.get('systemLanguage')
            if system_lang:
                existing_languages.add(system_lang)

        # Add missing translations
        for lang, translated_texts in available_translations.items():
            if lang in existing_languages:
                if overwrite:
                    # Find the existing translation node and update it
                    for text_elem in text_elements:
                        if text_elem.get('systemLanguage') == lang:
                            # Update the text content for each tspan
                            tspans = text_elem.xpath('./svg:tspan', namespaces={'svg': 'http://www.w3.org/2000/svg'})
                            if tspans and len(tspans) == len(translated_texts):
                                for i, tspan in enumerate(tspans):
                                    tspan.text = translated_texts[i]
                            elif not tspans and len(translated_texts) == 1:
                                text_elem.text = translated_texts[0]

                            stats['updated_translations'] += 1
                            logger.debug(f"Updated {lang} translation for '{default_texts}'")
                            break
                else:
                    stats['skipped_translations'] += 1
                    logger.debug(f"Skipped existing {lang} translation for '{default_texts}'")
            else:
                # Create a new translation node
                if not dry_run:
                    # Clone the default node
                    new_node = etree.Element(default_node.tag, attrib=default_node.attrib)

                    # Update attributes
                    new_node.set('systemLanguage', lang)

                    # Generate unique ID
                    original_id = default_node.get('id')
                    if original_id:
                        new_id = generate_unique_id(original_id, lang, existing_ids)
                        new_node.set('id', new_id)
                        existing_ids.add(new_id)

                    # Add the translation text for each tspan
                    tspans = default_node.xpath('./svg:tspan', namespaces={'svg': 'http://www.w3.org/2000/svg'})
                    if tspans and len(tspans) == len(translated_texts):
                        # Clone the tspan structure
                        for i, tspan in enumerate(tspans):
                            new_tspan = etree.Element(tspan.tag, attrib=tspan.attrib)
                            new_tspan.text = translated_texts[i]

                            # Generate unique ID for tspan
                            original_tspan_id = tspan.get('id')
                            if original_tspan_id:
                                new_tspan_id = generate_unique_id(original_tspan_id, lang, existing_ids)
                                new_tspan.set('id', new_tspan_id)
                                existing_ids.add(new_tspan_id)

                            new_node.append(new_tspan)
                    elif not tspans and len(translated_texts) == 1:
                        new_node.text = translated_texts[0]

                    # Insert the new node
                    switch.insert(0, new_node)

                stats['inserted_translations'] += 1
                logger.debug(f"Inserted {lang} translation for '{default_texts}'")

        stats['processed_switches'] += 1

    # Save data to JSON file
    output_dir = Path(__file__).parent / "translated"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / svg_file_path.name

    # Write the modified SVG
    tree.write(str(output_file), encoding='utf-8', xml_declaration=True, pretty_print=True)
    logger.info(f"Saved modified SVG to {output_file}")

    logger.info(f"Processed {stats['processed_switches']} switches")
    logger.info(f"Inserted {stats['inserted_translations']} translations")
    logger.info(f"Updated {stats['updated_translations']} translations")
    logger.info(f"Skipped {stats['skipped_translations']} existing translations")

    return stats


def main():
    # Set up logging
    logger = setup_logging(False)
    Dir = Path(__file__).parent
    data = extract(Dir / "files1/arabic.svg")
    print("______________________\n"*5)

    result = inject(Dir / "files1/no_translations.svg", [Dir / "data/arabic.svg.json"])

    print("______________________\n"*5)

    data2 = extract(Dir.parent / "big_example/file2.svg")
    print("______________________\n"*5)

    result2 = inject(Dir.parent / "big_example/file1.svg", [Dir / "data/file2.svg.json"])

    data = extract(Dir / "files2/from.svg")
    print("______________________\n"*5)

    result = inject(Dir / "files2/to.svg", [Dir / "data/from.svg.json"])


if __name__ == '__main__':
    sys.exit(main())
