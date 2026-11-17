from pathlib import Path

from directory_tree import DisplayTree

tree_work = {
    "tree.md": Path(__file__).parent.parent / "www/python/src",
    "main_app_tree.md": Path(__file__).parent.parent / "www/python/src/main_app",
    "test_tree.md": Path(__file__).parent.parent / "tests",
}

ignore_list = [
    "Domain_php_source.txt",
    "__pycache__",
    "old",
    "app1.py",
    "example.env",
    # "*.html",
    "*.php",
    "**/fixtures/output",
    "output",
    "results_api_php_code",
    "bs4_admin",
    "local.html",
    "local_not_sort.html",
    "local_not_sort_z.html",
    "ncc2c.html",
]

for tree_name, tree_path in tree_work.items():
    tree_save_path = Path(__file__).parent / tree_name

    _tree: str = DisplayTree(
        dirPath=str(tree_path),
        stringRep=True,
        header=False,
        maxDepth=float("inf"),
        showHidden=False,
        ignoreList=ignore_list,
        onlyFiles=False,
        onlyDirs=False,
        sortBy=2,
        raiseException=False,
        printErrorTraceback=False,
        spacing=True,
    )  # type: ignore

    tree_save_path.write_text(f"```\n{_tree}\n```", encoding="utf-8")
    print(f"Saved {tree_name}")
