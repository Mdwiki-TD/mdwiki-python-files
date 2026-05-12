from .all_articles import AllArticlesRecord
from .dashboard import (
    CategoryRecord,
    ProjectRecord,
)
from .metrics import (
    AssessmentRecord,
    RefsCountRecord,
    WordRecord,
)
from .pages import (
    InProcessRecord,
    PageRecord,
    PagesUsersToMainRecord,
    UserPageRecord,
)
from .public import (
    LangRecord,
    MdwikiRevidRecord,
    TranslateTypeRecord,
)
from .publish import ReportRecord
from .qid import (
    AllQidsExistRecord,
    AllQidsRecord,
    QidRecord,
)
from .setting import (
    LanguageSettingRecord,
)
from .users import (
    UserRecord,
)
from .views import (
    EnwikiPageviewRecord,
    ViewsNewAllRecord,
    ViewsNewRecord,
)

__all__ = [
    "AllArticlesRecord",
    "AllQidsExistRecord",
    "AllQidsRecord",
    "AssessmentRecord",
    "CategoryRecord",
    "EnwikiPageviewRecord",
    "InProcessRecord",
    "LangRecord",
    "LanguageSettingRecord",
    "MdwikiRevidRecord",
    "PageRecord",
    "PagesUsersToMainRecord",
    "ProjectRecord",
    "QidRecord",
    "RefsCountRecord",
    "ReportRecord",
    "TranslateTypeRecord",
    "UserPageRecord",
    "UserRecord",
    "ViewsNewAllRecord",
    "ViewsNewRecord",
    "WordRecord",
]
