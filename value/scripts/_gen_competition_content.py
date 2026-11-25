"""Generate EN/EL competition content files for Value wiki §06."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

# slug -> (competitor, case title EN, why title path)
CASES = [
    ("hr-presence", "Verkada", "Know who is present and who is not"),
    ("mall", "Quividi", "Screens that sell themselves"),
    ("shop-floor", "RetailNext", "See how shoppers move"),
    ("mall", "Quividi", "Screens that sell themselves"),  # duplicate guard — fixed below
]

# Rebuild clean list
CASES = [
    ("hr-presence", "Verkada", "Know who is present and who is not"),
    ("mall", "Quividi", "Screens that sell themselves"),
    ("shop-floor", "RetailNext", "See how shoppers move"),
    ("cottage", "Ring (Amazon)", "Peace of mind at home — and away"),
    ("home-care", "SafelyYou", "Hospital-grade care at home"),
    ("security", "LiveView Technologies (LVT)", "Night shifts that never blink"),
    ("shipping", "ShipIn", "Who’s onboard. Who’s on site. Who fell."),
    ("enterprise-perimeter", "Senstar", "Perimeters that detect, verify, and dispatch"),
    ("smart-city", "Genetec", "City cameras that decide and act"),
]

CASES_EL = {
    "hr-presence": ("Verkada", "Ξέρετε ποιός είναι παρόν και ποιος όχι"),
    "mall": ("Quividi", "Οθόνες που πουλάνε μόνες τους"),
    "shop-floor": ("RetailNext", "Δείτε πώς κινούνται οι πελάτες"),
    "cottage": ("Ring (Amazon)", "Ηρεμία στο σπίτι — και μακριά"),
    "home-care": ("SafelyYou", "Νοσοκομειακή φροντίδα στο σπίτι"),
    "security": ("LiveView Technologies (LVT)", "Νυχτερινές βάρδιες που επαγρυπνούν"),
    "shipping": ("ShipIn", "Ποιος είναι στην θέση του. Ποιος στον χώρο. Ποιος έπεσε."),
    "enterprise-perimeter": ("Senstar", "Περίμετροι που ανιχνεύουν, επαληθεύουν και αναπτύσσουν"),
    "smart-city": ("Genetec", "Κάμερες πόλης που αποφασίζουν και δρουν"),
}


def mark(ok: str) -> str:
    """ok: yes | partial | no"""
    if ok == "yes":
        return '<span class="tag ok">Yes</span>'
    if ok == "partial":
        return '<span class="tag mode">Partial</span>'
    return '<span class="tag">No</span>'


def mark_el(ok: str) -> str:
    if ok == "yes":
        return '<span class="tag ok">Ναι</span>'
    if ok == "partial":
        return '<span class="tag mode">Μερικώς</span>'
    return '<span class="tag">Όχι</span>'


# Feature rows: (label, eyenet, competitor) where eyenet/competitor are yes|partial|no
# Competitor cells vary by case — defined per case below.

FEATURES_EN = [
    "On-prem Detect → Decide → Act",
    "Any IP / Wi‑Fi / phone camera",
    "No per-camera license tax",
    "Cross-site Matrix / VPN mesh",
    "Offline / thin-link operation",
    "Vertical depth for this use case",
    "Cloud / bandwidth dependency",
    "Hardware lock-in",
]

FEATURES_EL = [
    "On-prem Detect → Decide → Act",
    "Οποιαδήποτε IP / Wi‑Fi / κάμερα τηλεφώνου",
    "Χωρίς φόρο άδειας ανά κάμερα",
    "Cross-site Matrix / VPN mesh",
    "Λειτουργία offline / λεπτού συνδέσμου",
    "Καθετοποίηση για αυτή την περίπτωση",
    "Εξάρτηση από cloud / bandwidth",
    "Κλείδωμα σε hardware",
]

# EyeNet column is constant across cases
EYENET_MARKS = ["yes", "yes", "yes", "yes", "yes", "yes", "no", "no"]
# Cloud dependency: EyeNet = No (doesn't depend). Hardware lock-in: EyeNet = No.

# Competitor marks per slug (same 8 rows)
COMP_MARKS = {
    "hr-presence": ["partial", "no", "no", "partial", "no", "yes", "yes", "yes"],  # Verkada cloud + own cams
    "mall": ["partial", "partial", "yes", "no", "partial", "yes", "partial", "no"],  # Quividi analytics
    "shop-floor": ["partial", "partial", "partial", "partial", "no", "yes", "yes", "partial"],  # RetailNext
    "cottage": ["partial", "no", "partial", "no", "partial", "yes", "yes", "yes"],  # Ring
    "home-care": ["partial", "no", "partial", "no", "partial", "yes", "partial", "yes"],  # SafelyYou
    "security": ["partial", "no", "partial", "partial", "partial", "yes", "yes", "yes"],  # LVT units
    "shipping": ["partial", "partial", "partial", "partial", "yes", "yes", "partial", "partial"],  # ShipIn
    "enterprise-perimeter": ["partial", "partial", "partial", "partial", "partial", "yes", "partial", "partial"],  # Senstar
    "smart-city": ["partial", "yes", "no", "yes", "partial", "yes", "partial", "no"],  # Genetec — open cams, license model
}


STORIES_EN = {
    "hr-presence": {
        "who": "Workplace security & facilities teams buying cloud cameras with people analytics.",
        "story": (
            "Verkada sells an integrated cloud physical-security platform — cameras, access, sensors, and "
            "People Analytics / occupancy — to enterprises that want dashboards without managing a VMS. "
            "It is strong at workplace presence and multi-site admin when buyers accept Verkada hardware "
            "and a cloud control plane. It does not position as an any-camera, on-prem Detect → Decide → Act "
            "stack for shipping, home care, city ops, and the rest of EyeNet’s cases."
        ),
        "financials": [
            ("Ownership", "Private (San Mateo, CA); founded 2016"),
            ("Valuation", "$5.8B (Dec 2025, CapitalG-led investment)"),
            ("Prior round", "Series E $200M at $4.5B (Feb 2025, General Catalyst)"),
            ("Scale signals", ">$500M 2024 revenue (press); >$1B annualized bookings (Dec 2025 company)"),
            ("Capital raised", ">$700M cumulative (company)"),
        ],
        "sources": "Verkada blog (Feb / Dec 2025); Reuters 3 Dec 2025; Fabrica Ventures May 2025.",
        "gap": "Cloud + proprietary device estate; presence analytics for workplaces — not a sovereign multi-vertical action fabric.",
    },
    "mall": {
        "who": "DOOH / retail-media publishers optimizing screen inventory with audience measurement.",
        "story": (
            "Quividi is a Paris-based computer-vision audience-intelligence vendor for digital out-of-home "
            "and retail media — impressions, dwell, and shopper engagement to monetize and optimize screens. "
            "It is a focused analytics layer for signage ROI, not an on-premises automation brain that also "
            "runs security, care, maritime, and city cases on the same installation."
        ),
        "financials": [
            ("Ownership", "Private SAS (Paris); founded 2006"),
            ("Published revenue", "€1.40M FY2024 (French company accounts)"),
            ("Funding", "~$1.4M historical (seed / 2016 venture); not a late-stage platform raise"),
            ("Footprint", "Audience measurement specialist for DOOH & retail media"),
        ],
        "sources": "French published accounts (SIREN 490 937 422) FY2024; company positioning.",
        "gap": "Audience metrics for screens — not Detect → Decide → Act across EyeNet’s broader case set.",
    },
    "shop-floor": {
        "who": "Retail chains buying in-store traffic, pathing, and conversion analytics.",
        "story": (
            "RetailNext provides in-store shopper analytics — traffic, dwell, pathing, and conversion "
            "insights for retailers. It is a mature vertical analytics franchise (and Battery Ventures–backed "
            "platform) optimized for retail ops dashboards. It is not an edge action system for night "
            "security, home care, perimeters, or fleets on one on-prem mesh."
        ),
        "financials": [
            ("Ownership", "Private; Battery Ventures private-equity involvement (2025)"),
            ("Revenue (est.)", "~$65M annual (third-party estimate — not audited disclosure)"),
            ("Funding", "~$226M total raised across rounds (third-party databases)"),
            ("Focus", "Retail traffic & path analytics"),
        ],
        "sources": "Third-party funding/revenue databases; Battery Ventures PE coverage 2025. Label estimates as non-diligence.",
        "gap": "Deep retail analytics cloud — not hardware-agnostic on-prem action across EyeNet use cases.",
    },
    "cottage": {
        "who": "Consumers and small properties wanting doorbell / outdoor cams with app alerts.",
        "story": (
            "Ring (Amazon) owns the consumer home-security camera and doorbell category — app-first "
            "alerts, neighborhood features, and Amazon retail distribution. It is the closest mass-market "
            "rival for home/away peace of mind. The model is cloud consumer devices and subscriptions, "
            "not an enterprise-grade any-camera on-prem fabric that also serves industrial and city buyers."
        ),
        "financials": [
            ("Ownership", "Amazon subsidiary (acquired Feb 2018, ~$1B reported)"),
            ("Revenue", "Not broken out in Amazon filings; third-party estimates often cite ~$600M class"),
            ("Model", "Hardware + Protect subscriptions; cloud video"),
            ("Scale", "Category-defining US consumer brand under Amazon Devices"),
        ],
        "sources": "Amazon acquisition press 2018; third-party revenue estimates (not Amazon segment disclosure).",
        "gap": "Consumer cloud cameras — not B2B/enterprise multi-vertical Detect → Decide → Act on-prem.",
    },
    "home-care": {
        "who": "Senior-living operators reducing falls and ER visits with room cameras + AI.",
        "story": (
            "SafelyYou leads camera-based fall detection and AI care tools for senior living (Respond, "
            "Clarity, Aware), pairing vision with remote clinical workflows. It is the closest rival for "
            "hospital-grade care monitoring. The stack is care-vertical and typically appliance/cloud "
            "oriented — not EyeNet’s cross-industry on-prem action platform."
        ),
        "financials": [
            ("Ownership", "Private (San Francisco); founded 2016"),
            ("Latest round", "Series C $43M (Jan 2025, Touring Capital)"),
            ("Total funding", ">$100M cumulative (company)"),
            ("Proof points", "Company claims ~40% fall reduction / ~80% fewer fall-related ER visits"),
        ],
        "sources": "SafelyYou / Business Wire 28 Jan 2025.",
        "gap": "Excellent care vertical depth — not a single brain for mall, maritime, perimeter, and city cases.",
    },
    "security": {
        "who": "Retail, construction, and site owners replacing or augmenting night guards with mobile towers.",
        "story": (
            "LiveView Technologies (LVT) sells rapidly deployable mobile security units with cameras, "
            "deterrence, and remote monitoring — a hardware+cloud answer to “eyes on site when posts are "
            "expensive.” It competes with EyeNet’s night-vigilance narrative via physical units and "
            "monitoring services, not via any-camera software that also runs home, care, and city cases."
        ),
        "financials": [
            ("Ownership", "Private (American Fork, UT)"),
            ("Funding", "~$117M VC since 2020; Series B $50M (Jun 2022, Sorenson Capital)"),
            ("Valuation", "Company stated >$1B valuation (Sep 2025 press); secondary estimates vary"),
            ("Growth", "Company: 483% revenue increase 2021–2024 (absolute revenue not disclosed)"),
        ],
        "sources": "LVT / GlobeNewswire Jun 2022; LVT president appointment press Sep 2025; Pulse2 interview Nov 2025.",
        "gap": "Mobile tower + monitoring estate — not software-only any-camera on-prem across EyeNet cases.",
    },
    "shipping": {
        "who": "Shipowners and shore ops wanting AI vision for safety and fleet performance.",
        "story": (
            "ShipIn’s FleetVision brings AI visual analytics to commercial vessels — safety events, "
            "ops anomalies, and ship–shore alignment. It is the closest maritime vision rival to EyeNet’s "
            "onboard/on-site presence and fall narrative. It remains a maritime platform, not a unified "
            "on-prem product for malls, homes, and city meshes."
        ),
        "financials": [
            ("Ownership", "Private (Boston / Newton, MA area)"),
            ("Series A", "$24M (Oct 2022, Zeev Ventures)"),
            ("Series B", "$52M (Aug 2026, Proofpoint Capital)"),
            ("Scale", "Company: ~92 shipowners / 1,300+ vessels (2026 financing coverage)"),
        ],
        "sources": "Ship-Technology / NBC Boston Oct 2022; Dealroom / Blank Rome Aug 2026.",
        "gap": "Maritime AI vision depth — not EyeNet’s across-case on-prem decide-and-act model.",
    },
    "enterprise-perimeter": {
        "who": "Critical infrastructure and industrial sites buying perimeter intrusion detection.",
        "story": (
            "Senstar (NASDAQ: SNT) provides perimeter intrusion detection, video, and access products "
            "for campuses, utilities, and industrial sites — virtual and physical perimeter sensing with "
            "a long security heritage. It is a natural rival for Detect → Dispatch on fences and zones. "
            "It does not claim EyeNet’s consumer-to-city software breadth on any camera without a "
            "perimeter-product SKU mindset."
        ),
        "financials": [
            ("Ownership", "Public — NASDAQ: SNT"),
            ("FY2024 revenue", "$35.8M (+9% YoY)"),
            ("FY2024 profit", "Net income $2.6M; EBITDA $4.6M"),
            ("Balance sheet", "Cash ~$20.5M, no debt (31 Dec 2024)"),
        ],
        "sources": "Senstar Technologies FY2024 results press release 23 Apr 2025.",
        "gap": "Strong perimeter product company — not a multi-vertical on-prem action OS for all EyeNet cases.",
    },
    "smart-city": {
        "who": "Cities and large enterprises standardizing on unified VMS / security platforms.",
        "story": (
            "Genetec (Montreal) builds Security Center — video, access, ALPR, and city-scale operations "
            "through partners, with on-prem and hybrid options and open camera support. It is the closest "
            "platform rival for multi-borough camera fabrics. Genetec is a classic VMS/security platform "
            "business (licenses, integrators), not EyeNet’s lean any-camera action appliance story across "
            "home, care, and SME cases as well."
        ),
        "financials": [
            ("Ownership", "Private; bootstrapped — company states no outside VC/PE"),
            ("Customers", ">42,500 organizations (company, 2025–2026)"),
            ("Headcount", "~2,100–2,600 employees (company / press)"),
            ("Revenue", "Not disclosed; third-party estimates often ~$300–400M — treat as estimate only"),
        ],
        "sources": "Genetec company materials; Safety Tech Review / press on customer count & bootstrap stance.",
        "gap": "Category-leading unified security platform — still a VMS-centric model, not EyeNet’s cross-case action fabric.",
    },
}

STORIES_EL_NOTES = {
    # Greek pages mirror structure; we'll generate from EN with Greek chrome + translated key paras
}


def feature_table_en(slug: str, competitor: str) -> str:
    rows = []
    for i, label in enumerate(FEATURES_EN):
        # For cloud dependency row, "yes" for competitor means they depend on cloud (bad for sovereignty)
        # Display as-is with marks
        e = EYENET_MARKS[i]
        c = COMP_MARKS[slug][i]
        # Invert display meaning for dependency/lock-in rows so Yes = has the problem
        if i >= 6:
            # show Yes = depends / locked — EyeNet No is good
            pass
        rows.append(
            f"<tr><td>{label}</td><td>{mark(e)}</td><td>{mark(c)}</td></tr>"
        )
    return f"""<table class="table-stack">
<thead><tr><th>Capability</th><th>EyeNet</th><th>{competitor}</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody>
</table>"""


def feature_table_el(slug: str, competitor: str) -> str:
    rows = []
    for i, label in enumerate(FEATURES_EL):
        e = EYENET_MARKS[i]
        c = COMP_MARKS[slug][i]
        rows.append(
            f"<tr><td>{label}</td><td>{mark_el(e)}</td><td>{mark_el(c)}</td></tr>"
        )
    return f"""<table class="table-stack">
<thead><tr><th>Ικανότητα</th><th>EyeNet</th><th>{competitor}</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody>
</table>"""


def fin_table_en(items: list[tuple[str, str]]) -> str:
    body = "".join(
        f'<tr class="{"row-accent" if i % 2 else ""}"><td>{k}</td><td>{v}</td></tr>'
        for i, (k, v) in enumerate(items)
    )
    return f"""<table class="table-stack">
<thead><tr><th>Metric</th><th>Figure (public / press)</th></tr></thead>
<tbody>{body}</tbody>
</table>"""


def fin_table_el(items: list[tuple[str, str]]) -> str:
    body = "".join(
        f'<tr class="{"row-accent" if i % 2 else ""}"><td>{k}</td><td>{v}</td></tr>'
        for i, (k, v) in enumerate(items)
    )
    return f"""<table class="table-stack">
<thead><tr><th>Μετρική</th><th>Στοιχείο (δημόσιο / τύπος)</th></tr></thead>
<tbody>{body}</tbody>
</table>"""


def case_en(slug: str, competitor: str, case_title: str, num: int) -> str:
    s = STORIES_EN[slug]
    return f"""<div class="kicker">Closest vertical rival for this EyeNet case — not a peer across all nine cases.</div>
<p class="page-lead"><a href="/why/{slug}/">EyeNet case {num:02d}: {case_title}</a> · Closest competitor: <strong>{competitor}</strong></p>

<div class="panel">
  <h4>Competitor story</h4>
  <p class="who">{s["who"]}</p>
  <p>{s["story"]}</p>
  <p><strong>Where they stop:</strong> {s["gap"]}</p>
</div>

<h3 class="sub">Recent financials</h3>
{fin_table_en(s["financials"])}
<p class="side-note"><strong>Sources:</strong> {s["sources"]} Figures are public/press estimates for orientation — not EyeNet diligence.</p>

<h3 class="sub">Feature comparison</h3>
{feature_table_en(slug, competitor)}
<p class="side-note">Shared capability rows across all nine rivalry pages. “Cloud / bandwidth dependency” and “Hardware lock-in”: <strong>Yes</strong> means the rival leans on that constraint; EyeNet aims for <strong>No</strong>.</p>
"""


# Greek translations of stories (concise professional)
STORIES_EL = {
    "hr-presence": {
        "who": "Ομάδες workplace security & facilities που αγοράζουν cloud κάμερες με people analytics.",
        "story": (
            "Η Verkada πουλάει ολοκληρωμένη cloud πλατφόρμα φυσικής ασφάλειας — κάμερες, access, αισθητήρες και "
            "People Analytics / occupancy — σε επιχειρήσεις που θέλουν dashboards χωρίς να διαχειρίζονται VMS. "
            "Είναι ισχυρή στην παρουσία χώρου εργασίας όταν ο αγοραστής δέχεται hardware Verkada και cloud control plane. "
            "Δεν τοποθετείται ως any-camera, on-prem Detect → Decide → Act για ναυτιλία, home care, πόλη και τις υπόλοιπες περιπτώσεις EyeNet."
        ),
        "gap": "Cloud + ιδιόκτητο device estate· analytics παρουσίας για workplaces — όχι sovereign multi-vertical action fabric.",
        "fin_labels": ("Ιδιοκτησία", "Αποτίμηση", "Προηγούμενος γύρος", "Σήματα κλίμακας", "Κεφάλαια"),
    },
    "mall": {
        "who": "Εκδότες DOOH / retail media που βελτιστοποιούν οθόνες με μέτρηση κοινού.",
        "story": (
            "Η Quividi (Παρίσι) είναι vendor computer-vision audience intelligence για digital out-of-home και retail media — "
            "impressions, dwell και engagement για monetization οθονών. Είναι εστιασμένο analytics layer για ROI signage, "
            "όχι on-premises automation brain που τρέχει και ασφάλεια, φροντίδα, ναυτιλία και πόλη στην ίδια εγκατάσταση."
        ),
        "gap": "Μετρικές κοινού για οθόνες — όχι Detect → Decide → Act σε όλο το σύνολο περιπτώσεων EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Δημοσιευμένος τζίρος", "Χρηματοδότηση", "Εστίαση"),
    },
    "shop-floor": {
        "who": "Αλυσίδες retail που αγοράζουν traffic, pathing και conversion analytics.",
        "story": (
            "Η RetailNext παρέχει in-store shopper analytics — traffic, dwell, pathing και conversion για retailers. "
            "Είναι ώριμο vertical analytics franchise (με συμμετοχή Battery Ventures) για retail dashboards. "
            "Δεν είναι edge action σύστημα για νυχτερινή ασφάλεια, home care, περιμέτρους ή στόλους σε ένα on-prem mesh."
        ),
        "gap": "Βαθύ retail analytics cloud — όχι hardware-agnostic on-prem δράση στις περιπτώσεις EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Έσοδα (εκτ.)", "Χρηματοδότηση", "Εστίαση"),
    },
    "cottage": {
        "who": "Καταναλωτές και μικρά ακίνητα που θέλουν κουδούνι / εξωτερικές κάμερες με app alerts.",
        "story": (
            "Η Ring (Amazon) κυριαρχεί στην κατηγορία consumer home-security camera και doorbell — app alerts, "
            "neighborhood features και διανομή Amazon. Είναι ο πλησιέστερος mass-market αντίπαλος για ηρεμία σπιτιού. "
            "Το μοντέλο είναι cloud consumer devices και συνδρομές, όχι enterprise any-camera on-prem fabric."
        ),
        "gap": "Consumer cloud κάμερες — όχι B2B/enterprise multi-vertical Detect → Decide → Act on-prem.",
        "fin_labels": ("Ιδιοκτησία", "Έσοδα", "Μοντέλο", "Κλίμακα"),
    },
    "home-care": {
        "who": "Operators senior living που μειώνουν πτώσεις και επισκέψεις ΕΡ με κάμερες + AI.",
        "story": (
            "Η SafelyYou ηγείται στην ανίχνευση πτώσης με κάμερα και AI εργαλεία φροντίδας για senior living "
            "(Respond, Clarity, Aware). Είναι ο πλησιέστερος αντίπαλος για νοσοκομειακή παρακολούθηση φροντίδας. "
            "Το stack είναι care-vertical — όχι η cross-industry on-prem πλατφόρμα του EyeNet."
        ),
        "gap": "Εξαιρετικό βάθος στο care — όχι ένας εγκέφαλος για mall, ναυτιλία, περίμετρο και πόλη.",
        "fin_labels": ("Ιδιοκτησία", "Τελευταίος γύρος", "Συνολική χρηματοδότηση", "Αποδείξεις"),
    },
    "security": {
        "who": "Retail, κατασκευές και χώροι που αντικαθιστούν νυχτερινούς φύλακες με mobile towers.",
        "story": (
            "Η LiveView Technologies (LVT) πουλάει ταχέως αναπτυσσόμενες κινητές μονάδες ασφάλειας με κάμερες, "
            "αποτροπή και remote monitoring — hardware+cloud απάντηση όταν τα πόστα είναι ακριβά. "
            "Ανταγωνίζεται το αφήγημα νυχτερινής επαγρύπνησης του EyeNet μέσω φυσικών μονάδων, όχι μέσω any-camera software."
        ),
        "gap": "Mobile tower + monitoring — όχι software-only any-camera on-prem στις περιπτώσεις EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Χρηματοδότηση", "Αποτίμηση", "Ανάπτυξη"),
    },
    "shipping": {
        "who": "Πλοιοκτήτες και shore ops που θέλουν AI όραση για ασφάλεια και απόδοση στόλου.",
        "story": (
            "Το FleetVision της ShipIn φέρνει AI visual analytics σε εμπορικά πλοία — συμβάντα ασφαλείας, "
            "ανωμαλίες ops και ευθυγράμμιση πλοίου–ξηράς. Είναι ο πλησιέστερος ναυτιλιακός αντίπαλος στο αφήγημα "
            "παρουσίας/πτώσης του EyeNet. Παραμένει ναυτιλιακή πλατφόρμα, όχι ενιαίο on-prem προϊόν για malls, σπίτια και πόλεις."
        ),
        "gap": "Βάθος ναυτιλιακής AI όρασης — όχι το across-case on-prem μοντέλο του EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Series A", "Series B", "Κλίμακα"),
    },
    "enterprise-perimeter": {
        "who": "Κρίσιμες υποδομές και βιομηχανία που αγοράζουν perimeter intrusion detection.",
        "story": (
            "Η Senstar (NASDAQ: SNT) παρέχει perimeter intrusion detection, video και access για campuses, "
            "utilities και βιομηχανία — εικονική και φυσική περίμετρος με μακρά κληρονομιά ασφάλειας. "
            "Είναι φυσικός αντίπαλος για Detect → Dispatch σε φράχτες και ζώνες. Δεν διεκδικεί το εύρος λογισμικού EyeNet από consumer έως πόλη."
        ),
        "gap": "Ισχυρή εταιρεία perimeter προϊόντων — όχι multi-vertical on-prem action OS για όλες τις περιπτώσεις EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Έσοδα FY2024", "Κέρδη FY2024", "Ισολογισμός"),
    },
    "smart-city": {
        "who": "Πόλεις και μεγάλοι οργανισμοί που τυποποιούν σε unified VMS / security platforms.",
        "story": (
            "Η Genetec (Μόντρεαλ) χτίζει το Security Center — video, access, ALPR και λειτουργίες πόλης μέσω partners, "
            "με on-prem και hybrid επιλογές και ανοιχτή υποστήριξη καμερών. Είναι ο πλησιέστερος platform αντίπαλος "
            "για meshes πολλών συνοικιών. Παραμένει κλασική VMS/security πλατφόρμα (άδειες, integrators), "
            "όχι το lean any-camera action αφήγημα του EyeNet και για home, care και SME."
        ),
        "gap": "Κορυφαία unified security πλατφόρμα — ακόμα VMS-centric μοντέλο, όχι cross-case action fabric EyeNet.",
        "fin_labels": ("Ιδιοκτησία", "Πελάτες", "Προσωπικό", "Έσοδα"),
    },
}


def case_el(slug: str, competitor: str, case_title: str, num: int) -> str:
    en = STORIES_EN[slug]
    el = STORIES_EL[slug]
    # Keep English financial values; Greek labels
    labeled = list(zip(el["fin_labels"], [v for _, v in en["financials"]]))
    return f"""<div class="kicker">Ο πλησιέστερος κάθετος αντίπαλος για αυτή την περίπτωση EyeNet — όχι peer και στις εννέα.</div>
<p class="page-lead"><a href="/el/why/{slug}/">Περίπτωση EyeNet {num:02d}: {case_title}</a> · Πλησιέστερος ανταγωνιστής: <strong>{competitor}</strong></p>

<div class="panel">
  <h4>Η ιστορία του ανταγωνιστή</h4>
  <p class="who">{el["who"]}</p>
  <p>{el["story"]}</p>
  <p><strong>Πού σταματούν:</strong> {el["gap"]}</p>
</div>

<h3 class="sub">Πρόσφατα οικονομικά</h3>
{fin_table_el(labeled)}
<p class="side-note"><strong>Πηγές:</strong> {en["sources"]} Τα στοιχεία είναι δημόσια/τύπου για προσανατολισμό — όχι diligence του EyeNet.</p>

<h3 class="sub">Σύγκριση χαρακτηριστικών</h3>
{feature_table_el(slug, competitor)}
<p class="side-note">Κοινές γραμμές ικανοτήτων και στις εννέα σελίδες. «Εξάρτηση από cloud / bandwidth» και «Κλείδωμα σε hardware»: το <strong>Ναι</strong> σημαίνει ότι ο αντίπαλος βασίζεται σε αυτό· το EyeNet στοχεύει σε <strong>Όχι</strong>.</p>
"""


def index_en() -> str:
    rows = "".join(
        f'<tr class="{"row-accent" if i % 2 else ""}"><td><a href="/competition/{slug}/">{title}</a></td>'
        f"<td><strong>{comp}</strong></td></tr>"
        for i, (slug, comp, title) in enumerate(CASES)
    )
    cards = "".join(
        f'<a class="landing-card" href="/competition/{slug}/">'
        f'<span class="num">{i+1:02d}</span><strong>{title}</strong>'
        f"<span>Closest rival: {comp}</span></a>"
        for i, (slug, comp, title) in enumerate(CASES)
    )
    return f"""<div class="kicker">Rivals win vertical slices. None ship EyeNet’s across-case on-prem Detect → Decide → Act model.</div>
<p class="page-lead">Incumbents are real <strong>per use case</strong> — home cams, retail analytics, maritime AI, perimeter products, city VMS platforms. Each is optimized for one slice. EyeNet’s thesis: any IP camera, on-premises action, no per-camera tax, Matrix/VPN multi-site — one fabric across all nine cases below.</p>

<table class="table-stack">
<thead><tr><th>EyeNet case</th><th>Closest competitor</th></tr></thead>
<tbody>{rows}</tbody>
</table>

<div class="landing-cards" style="margin-top:14px">{cards}</div>
<p class="side-note">Each page: competitor story, recent public financials with sources, and a shared feature comparison table versus EyeNet.</p>
"""


def index_el() -> str:
    rows = "".join(
        f'<tr class="{"row-accent" if i % 2 else ""}"><td><a href="/el/competition/{slug}/">{CASES_EL[slug][1]}</a></td>'
        f"<td><strong>{CASES_EL[slug][0]}</strong></td></tr>"
        for i, (slug, _, _) in enumerate(CASES)
    )
    cards = "".join(
        f'<a class="landing-card" href="/el/competition/{slug}/">'
        f'<span class="num">{i+1:02d}</span><strong>{CASES_EL[slug][1]}</strong>'
        f"<span>Πλησιέστερος αντίπαλος: {CASES_EL[slug][0]}</span></a>"
        for i, (slug, _, _) in enumerate(CASES)
    )
    return f"""<div class="kicker">Οι αντίπαλοι κερδίζουν κάθετες φέτες. Κανείς δεν προσφέρει το across-case on-prem Detect → Decide → Act μοντέλο του EyeNet.</div>
<p class="page-lead">Οι incumbents είναι πραγματικοί <strong>ανά περίπτωση χρήσης</strong> — κάμερες σπιτιού, retail analytics, ναυτιλιακή AI, προϊόντα περιμέτρου, city VMS. Καθένας βελτιστοποιεί μία φέτα. Η θέση του EyeNet: οποιαδήποτε IP κάμερα, on-premises δράση, χωρίς φόρο ανά κάμερα, Matrix/VPN multi-site — ένα ύφασμα και στις εννέα περιπτώσεις.</p>

<table class="table-stack">
<thead><tr><th>Περίπτωση EyeNet</th><th>Πλησιέστερος ανταγωνιστής</th></tr></thead>
<tbody>{rows}</tbody>
</table>

<div class="landing-cards" style="margin-top:14px">{cards}</div>
<p class="side-note">Κάθε σελίδα: ιστορία ανταγωνιστή, πρόσφατα δημόσια οικονομικά με πηγές, και κοινό πίνακα σύγκρισης χαρακτηριστικών έναντι του EyeNet.</p>
"""


def main() -> None:
    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / "competition-index-en.html").write_text(index_en(), encoding="utf-8")
    (CONTENT / "competition-index-el.html").write_text(index_el(), encoding="utf-8")
    print("wrote competition-index-en/el.html")
    for i, (slug, comp, title) in enumerate(CASES, start=1):
        (CONTENT / f"competition-{slug}-en.html").write_text(
            case_en(slug, comp, title, i), encoding="utf-8"
        )
        el_comp, el_title = CASES_EL[slug]
        (CONTENT / f"competition-{slug}-el.html").write_text(
            case_el(slug, el_comp, el_title, i), encoding="utf-8"
        )
        print(f"wrote competition-{slug}-en/el.html")


if __name__ == "__main__":
    main()
