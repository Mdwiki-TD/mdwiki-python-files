# خطة الهجرة واستبدال استخدام mdapi_sql/services بنظام SQLAlchemy الجديد

تهدف هذه الخطة إلى تفصيل عملية استبدال المكونات القديمة المبنية على الاستعلامات المباشرة (Raw SQL) المتمثلة في `src/db/mdapi_sql/services/` والاعتماد بشكل كامل على نظام الخدمات الجديد المبني على **SQLAlchemy ORM** والموجود تحت `src/db/tools/services/`.

---

## 1. الأهداف والفوائد
* **أمان البيانات**: التخلص الكامل من احتمالية ثغرات حقن استعلامات SQL (SQL Injection).
* **إدارة الاتصال**: الاستفادة من ميزة تجميع الاتصالات (Connection Pooling) التي يوفرها SQLAlchemy بدلاً من فتح وإغلاق الاتصال مع كل استعلام.
* **جودة الشيفرة وقابليتها للصيانة**: استخدام الكائنات البرمجية المقابلة للجداول (ORM Models) مما يسهل عمليات التطوير وفحص الكود (Testing).
* **التكامل مع الاختبارات**: سهولة إجراء اختبارات الوحدات (Unit Tests) باستخدام قواعد بيانات وهمية في الذاكرة (SQLite in-memory) لخدمات SQLAlchemy.

---

## 2. جدول مطابقة الدوال والملفات (Mapping Table)

### أ. ملف `sql_qids.py` -> `qid_service.py`
المسار القديم: `src/db/mdapi_sql/services/sql_qids.py`
المسار الجديد: `src/db/tools/services/wikidata/qid_service.py`

| الدالة القديمة | البديل باستخدام SQLAlchemy / الدالة الجديدة | ملاحظات / خطة التعديل |
| :--- | :--- | :--- |
| `get_all_qids()` | `get_title_to_qid()` | ترجع قاموساً يربط العناوين بمعرفات QID مباشرة باستخدام الاستعلام عبر الـ ORM. |
| `add_qid(title, qid)` | `insert(title, qid)` أو `add_qid(title, qid)` | تقوم بالإدخال والتحقق من عدم الوجود المسبق. سنقوم بدعم معايير الفحص الإضافية في الخدمة الجديدة. |
| `set_qid_where_qid(new_qid, old_qid)` | دالة جديدة: `set_qid_where_qid(new_qid, old_qid)` | تحديث جميع السجلات التي تمتلك معرف QID قديم إلى المعرف الجديد باستخدام `session.query(QidRecord).filter(...)`. |
| `set_qid_where_title(title, qid)` | `add_qid(title, qid)` أو دالة مخصصة | تحديث المعرف بناءً على عنوان الصفحة. |
| `delete_title_from_db(title)` | دالة جديدة: `delete_by_title(title)` | حذف السجل المطابق للعنوان باستخدام `session.query(QidRecord).filter_by(title=title).delete()`. |
| `set_title_where_qid(new_title, qid)` | دالة جديدة: `set_title_where_qid(new_title, qid)` | تحديث عنوان الصفحة المقترن بالـ QID. |
| `qids_set_title_where_title_qid(...)` | دالة جديدة: `set_title_where_title_qid(...)` | تحديث مخصص للعنوان لـ QID محدد وعنوان قديم معين. |
| `add_titles_to_qids(tab0, add_empty_qid)`| دالة جديدة: `add_titles_to_qids(...)` | نقل نفس المنطق البرمجي للتحقق من العناوين وإضافتها دفعة واحدة باستخدام الـ ORM وإدارتها ضمن جلسة عمل (Session) واحدة لضمان الأداء العالي. |

---

### ب. ملف `sql_qids_others.py` -> `qid_others_service.py`
المسار القديم: `src/db/mdapi_sql/services/sql_qids_others.py`
المسار الجديد: `src/db/tools/services/wikidata/qid_others_service.py`

| الدالة القديمة | البديل باستخدام SQLAlchemy / الدالة الجديدة | ملاحظات / خطة التعديل |
| :--- | :--- | :--- |
| `get_others_qids()` | `get_title_to_qid()` | مستقاة بالكامل من جدول `qids_others` عبر الـ ORM. |
| `add_qid(title, qid)` | `insert(title, qid)` أو `add_qid_other(title, qid)` | تقوم بالإدخال والتحقق من عدم الوجود المسبق في كلا الجدولين. |
| `set_qid_where_qid(new_qid, old_qid)` | دالة جديدة: `set_qid_where_qid(...)` | تحديث السجلات في جدول `qids_others` عبر الاستعلام المباشر بالـ ORM. |
| `set_qid_where_title(title, qid)` | دالة جديدة أو استخدام `add_qid_other` | تحديث المعرف بناءً على عنوان الصفحة. |
| `delete_title_from_db(title)` | دالة جديدة: `delete_by_title(title)` | حذف السجل المطابق للعنوان من جدول `qids_others`. |
| `set_title_where_qid(new_title, qid)` | دالة جديدة: `set_title_where_qid(...)` | تحديث عنوان الصفحة المقترن بالـ QID في جدول `qids_others`. |
| `qids_set_title_where_title_qid(...)` | دالة جديدة | تحديث مخصص للعنوان لـ QID وعنوان قديم في جدول `qids_others`. |
| `add_titles_to_qids(...)` | دالة جديدة | نقل المنطق الذكي للإضافات الدفعية لجدول `qids_others`. |

---

### ج. ملف `sql_for_mdwiki.py` -> خدمات نطاقات SQLAlchemy المتعددة
المسار القديم: `src/db/mdapi_sql/services/sql_for_mdwiki.py`
المسار الجديد: موزعة على خدمات النطاقات في `src/db/tools/services/`

| الدالة القديمة في `sql_for_mdwiki.py` | الخدمة البديلة في نظام SQLAlchemy الجديد | ملاحظات ومسار الاستبدال |
| :--- | :--- | :--- |
| `mdwiki_sql` / `mdwiki_sql_dict` | `get_session()` مع تنفيذ استعلام نصي (Raw Text execution) أو استخدام الـ ORM مباشرة | لا يجب استخدام الاستعلامات المباشرة إلا للضرورة القصوى. يُفضل تحويل كل استعلام إلى ما يقابله من كائنات ORM. |
| `get_all_pages()` | `pages/page_service.py` -> `list_pages()` | يمكن تصفية العناوين فقط كـ `[p.title for p in list_pages()]` أو إضافة دالة خفيفة مخصصة للعناوين فقط لتقليل استهلاك الذاكرة. |
| `get_all_from_table(table_name)` | استعلام ORM عام أو دالة مخصصة لكل جدول | جلب البيانات باستخدام كائن الـ Model المقابل لاسم الجدول مثل `session.query(Model).distinct().all()`. |
| `get_all_pages_all_keys(...)` | `pages/page_service.py` / `pages/user_page_service.py` | استخدام `list_pages()` أو `list_user_pages()` وتصفيتها باللغة المطلوبة عبر فلتر SQLAlchemy. |
| `get_db_categories()` | `content/category_service.py` -> `list_categories()` | قراءة الجداول ككائنات `CategoryRecord` وتحويلها لقاموس يربط التصنيف بالعمق (depth). |
| `get_db_category_members()` | خدمة جديدة في `content/category_service.py` أو الـ Model المقابل | الاستعلام عن علاقة التصنيفات بالصفحات عبر الـ ORM المخصص لـ `category_members` لتحسين جودة الترابط. |
| `get_db_users()` | `pages/user_page_service.py` أو دالة مستخدم مخصصة | جلب قائمة أسماء المستخدمين المميزين المسجلين في جدول `users`. |
| `set_target_where_id(new_target, iid)` | `pages/page_service.py` -> `update_page(page_id=iid, target=new_target)` | تعديل السجل وتحديث حقل `target` وحقل `pupdate` تلقائياً عبر الـ ORM. |
| `set_deleted_where_id(iid)` | `pages/page_service.py` -> `update_page(page_id=iid, deleted=1)` | وسم الصفحة كـ "محذوفة" من خلال تحديث حقل `deleted` المقابل للـ ID المعطى. |
| `insert_to_pages_users_to_main(...)` | `reports/pages_users_to_main_service.py` -> `add_pages_users_to_main(...)` | إدراج السجل الجديد والتحقق من نجاح العملية باستخدام الـ ORM. |
| `add_new_to_pages(tab)` | `pages/page_service.py` -> `add_page(...)` أو `add_translate_row_to_db(...)` | استخدام دوال الإضافة الجاهزة في خدمة الصفحات والتي تتكفل بالتعامل مع التواريخ والتحققات التلقائية. |

---

## 3. خطوات التنفيذ التدريجي (Implementation Phases)

### المرحلة الأولى: تحديث وتحضير خدمات SQLAlchemy (Enhancement Phase)
1. **تحديث `qid_service.py` و `qid_others_service.py`**:
   - إضافة الدوال الغائبة مثل تحديث الـ QID أو العنوان بناءً على الـ QID، وحذف العناوين.
   - نقل منطق `add_titles_to_qids` الذكي الذي يمنع التكرارات ويسرع الإدخال ليعمل بالكامل عبر الـ ORM.
2. **تحديث خدمات الصفحات والتصنيفات**:
   - إضافة دالة `get_db_categories()` في `category_service.py` لترجع قاموس التصنيفات وعمقها مباشرة تسهيلاً لعملية الاستبدال السريع.
   - كتابة خدمات لإدارة `category_members` وجلب أعضاء التصنيفات ككائنات ORM.

### المرحلة الثانية: استبدال الاستدعاءات في الـ Bots والـ Scripts (Refactoring Callers)
البحث عن كافة الملفات التي تستورد من `db.mdapi_sql.services` وتغييرها لتستورد من الخدمات المقابلة في `db.tools.services`.

أمثلة على الاستبدال:

* **تعديل استيراد معرفات الويكي بيانات (Wikidata QIDs)**:
  ```python
  # القديم
  from db.mdapi_sql.services import sql_qids, sql_qids_others

  # الجديد
  from db.tools.services.wikidata import qid_service, qid_others_service
  ```

* **تعديل استيراد خدمات صفحات mdwiki**:
  ```python
  # القديم
  from db.mdapi_sql.services import sql_for_mdwiki

  # الجديد
  from db.tools.services.pages import page_service
  from db.tools.services.content import category_service
  ```

### المرحلة الثالثة: إزالة المكونات القديمة بالكامل (Cleanup Phase)
1. بعد تحويل كافة الملفات والتأكد من عدم وجود أي استدعاء يشير إلى `src/db/mdapi_sql/` أو ملفاتها الداخلية.
2. إزالة المجلد `src/db/mdapi_sql/` من شجرة المشروع نهائياً لتفادي وجود أكواد مكررة أو غير مستخدمة.

---

## 4. استراتيجية فحص الكود وضمان الجودة (Testing & Quality Assurance)
* **كتابة اختبارات الوحدات (Unit Tests)**:
  - إضافة اختبارات وحدات في مجلد `tests/` للتحقق من أن الخدمات الجديدة في SQLAlchemy تعطي نفس النتائج تماماً للبيانات المدخلة مقارنة بالدوال القديمة.
* **الاختبار اليدوي لبعض المهام (Smoke Testing)**:
  - تشغيل عينة من الـ bots والـ scripts المعدلة والتأكد من عدم حدوث أي خطأ متعلق بالاتصال بقاعدة البيانات أو معالجة الحقول.
* **الفحص التلقائي (Automated Verification)**:
  - تشغيل أداة `pytest` للتحقق من سلامة كافة الاختبارات وتوافقها مع التغييرات المطبقة.
