#!/usr/bin/env python3
"""Write Greek case-page overrides for value Most Valuable Cases."""

from __future__ import annotations

from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "content"

CASES: dict[str, str] = {}

CASES["why-hr-presence-el.html"] = """\
<article class="case-page" id="wedge-hr">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/hr-presence.png" alt="EyeNet παρουσία προσωπικού" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 01</span>
          <h2>Ξέρετε ποιός είναι παρόν και ποιος όχι</h2>
          <p class="who">Σπίτι · γραφείο · αποθήκη · βιομηχανία · ναυτιλία · ασφάλεια — ένα ευέλικτο εργαλείο Presence</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Η Presence είναι ένα ευέλικτο εργαλείο machine vision εξίσου κατάλληλο για έξυπνο κουδούνι στο σπίτι, γραφεία, αποθήκες, βιομηχανικούς ορόφους, πλοία και θέσεις ασφαλείας. Το EyeNet δείχνει ποιος είναι μέσα, πού και πότε — αυτόματα — ώστε οι ομάδες να σταματήσουν το κυνήγι παρουσιών και badges. Connectors με συστήματα CRM, όπως το HubSpot, κρατούν presence grants και επαφές συγχρονισμένα καθώς οι άνθρωποι μετακινούνται.</p>
          <ul class="case-features">
            <li><strong>Έξυπνο κουδούνι</strong> — ποιος είναι στην πόρτα στο σπίτι· παρουσία χωρίς cloud video</li>
            <li><strong>Stations εισόδου / εξόδου</strong> — Presence stations στις πόρτες για check-in / check-out</li>
            <li><strong>Κάμερες Vprofile</strong> — γραφεία, αποθήκες, βιομηχανικοί όροφοι και θέσεις φρουράς</li>
            <li><strong>Εφαρμογές Presence</strong> — κινητά και PCs προσωπικού</li>
            <li><strong>Ναυτιλία &amp; θέσεις ασφαλείας</strong> — το ίδιο stack για πλήρωμα, βάρδιες και περίμετρο</li>
            <li><strong>Hands-off ops</strong> — καθαρά αυτόματο· χωρίς χειροκίνητο roll-call ή κυνήγι</li>
            <li><strong>CRM Connectors</strong> — π.χ. HubSpot CRM connector: συγχρονισμός επαφών, post grants στο HubSpot σε πραγματικό χρόνο</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Ένα ευέλικτο εργαλείο machine vision Presence εξίσου κατάλληλο για σπίτι, γραφείο, αποθήκη, βιομηχανία, ναυτιλία και ασφάλεια — ποιος είναι μέσα, πού και πότε — χωρίς τριβή μόνο-badge ή παρουσίες σε spreadsheet.</p>
          <div class="tags">
            <span class="tag category">σπίτι</span>
            <span class="tag category">γραφείο</span>
            <span class="tag category">αποθήκη</span>
            <span class="tag category">βιομηχανία</span>
            <span class="tag category">ναυτιλία</span>
            <span class="tag category">ασφάλεια</span>
            <span class="tag">Presence</span>
            <span class="tag mode">Stations</span>
            <span class="tag mode">Vprofile</span>
            <span class="tag">Mobile · PC apps</span>
            <span class="tag user">HubSpot CRM</span>
          </div>
          <p class="side-note"><strong>CRM διαδρομή:</strong> πρώτα HubSpot· περαιτέρω CRM connectors ακολουθούν το ίδιο μοτίβο.</p>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Εργαζόμενος (επιβεβαιώσεις Presence app)</li>
            <li>Προϊστάμενος (εξαιρέσεις / καθυστέρηση / απουσία)</li>
            <li>HR / People ops (συχνές αναφορές παρουσίας, σχεδόν πραγματικού χρόνου, ημερήσιες, εβδομαδιαίες, μηνιαίες, παραμετροποιήσιμες κ.λπ.)</li>
            <li>Εγκαταστάσεις · timeline επαφής CRM (grants)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>HR manager</strong> μπορεί πλέον να αφήσει κάθε εργαζόμενο να κάνει check-in από το δικό του PC ή τηλέφωνο — και να στέλνει presence grants στο ERP/CRM — χωρίς νέο hardware, ακόμα και σε χιλιάδες θέσεις.</p>
      </div>
    </article>
"""

CASES["why-mall-el.html"] = """\
<article class="case-page" id="wedge-signage">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/mall-signage.png" alt="EyeNet Vision-adaptive Intelligent Signage" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 02</span>
          <h2>Οθόνες που πουλάνε μόνες τους</h2>
          <p class="who">Retail · χώροι · agencies · brand studios · operators digital signage</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Οι στατικές οθόνες καίνε budget επειδή κανείς δεν αποδεικνύει ποιος είδε τι. Το EyeNet διαβάζει τον χώρο — ηλικία, φύλο, μέγεθος ομάδας — και οδηγεί playlists από ζωντανά audience signals σε milliseconds. Η επισκεψιμότητα, οι πελάτες που περνάνε ή και που στέκονται μετατρέπουν διαδρόμους και spots σε μετρήσιμο marketing studio αντί για εικασίες.</p>
          <ul class="case-features">
            <li><strong>Διάβασμα χώρου</strong> — ηλικία, φύλο, μέγεθος ομάδας οδηγούν αλλαγές playlist σε milliseconds</li>
            <li><strong>Μηδέν έρευνες</strong> — γνωρίζετε ποιος βλέπει κάθε οθόνη: views, dwell, engagement</li>
            <li><strong>A/B στο πεδίο</strong> — εναλλαγή περιεχομένου με ζωντανά δεδομένα και αναφορές συμπεριφοράς κοινού· μέτρηση τι μετατρέπει</li>
            <li><strong>Signage ως studio</strong> — κάθε οθόνη γίνεται ένα μετρήσιμο και «ζωντανό» marketing εργαλείο σε διαδρόμους, καταστήματα και spots</li>
            <li><strong>Απόδειξη ROI</strong> — αναφορές impressions, engagement rates, funnels footfall-to-sales</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Οι στατικές οθόνες καίνε budget. Το Vision-adaptive Intelligent Signage μετατρέπει την κίνηση σε μετρήσιμη marketing νοημοσύνη — περιεχόμενο που αντιδρά και αριθμοί που δικαιολογούν τη δαπάνη.</p>
          <div class="tags">
            <span class="tag category">κατάστημα</span>
            <span class="tag category">marketing</span>
            <span class="tag">Signage</span>
            <span class="tag">Automation</span>
            <span class="tag mode">Spot · Gate · Area</span>
            <span class="tag user">Demographics</span>
            <span class="tag ok">ROI · A/B</span>
          </div>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Marketing manager (digests καμπάνιας / ROI)</li>
            <li>Content / media ops (playlist &amp; A/B triggers)</li>
            <li>Λειτουργίες χώρου / καταστήματος</li>
            <li>Agency · brand partner (προγραμματισμένες αναφορές)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>ιδιοκτήτης καταστήματος / mall</strong> μπορεί πλέον να δει ποιος κοιτάζει κάθε οθόνη — και να αλλάξει playlist με αποδεδειγμένα impressions — στις κάμερες που ήδη υπάρχουν στις οθόνες ή σε φθηνό πρόσθετο, χωρίς κλειδωμένο player kit ή SaaS φόρο ανά οθόνη.</p>
      </div>
    </article>
"""

CASES["why-shop-floor-el.html"] = """\
<article class="case-page" id="wedge-shop">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/shop-floor.jpg" alt="EyeNet κίνηση πελατών σε κατάστημα" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 03</span>
          <h2>Δείτε πώς κινούνται οι πελάτες</h2>
          <p class="who">Διευθυντές καταστήματος · store ops · πολυτοπικό retail</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Οι διευθυντές καταστήματος χρειάζονται να ξέρουν πώς κινούνται οι πελάτες στον χώρο — όχι μόνο ότι κάποιος μπήκε. Το EyeNet μετατρέπει τις υπάρχουσες κάμερες σε μετρήσεις ανθρώπων, διαδρομές, heatmaps, dwell και occupancy, με behavioural alerts όταν οι ζώνες γεμίζουν ή αδειάζουν. Οι managers παίρνουν συνοπτικές αναφορές και «ζωντανές» ειδοποιήσεις· το video δεν χρειάζεται να φύγει από το κατάστημα.</p>
          <ul class="case-features">
            <li><strong>Μέτρηση ανθρώπων</strong> — Face / Body / Both σε εισόδους και κάμερες ορόφου</li>
            <li><strong>Διαδρομές &amp; heatmaps</strong> — πώς κινούνται οι πελάτες σε διαδρόμους και ζώνες</li>
            <li><strong>Occupancy &amp; peaks</strong> — ώρες αιχμής ανά περιοχή, χωρίς εικασίες</li>
            <li><strong>Dwell &amp; επισκέψεις</strong> — πού μένουν οι αγοραστές vs πού περνούν</li>
            <li><strong>Behavioural alerts</strong> — occupancy / dwell / path / co-presence → mobile, email, webhook</li>
            <li><strong>On-prem ιδιωτικότητα</strong> — το video μένει τοπικά· οι managers παίρνουν digests και alerts, όχι cloud footage</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Μετατρέψτε μια απλή εγκατάσταση καμερών σε νοημοσύνη ορόφου με μετρήσεις, διαδρομές, αναφορές και ειδοποιήσεις. Η εγκατάσταση EyeNet στο κατάστημα αποδεικνύει πώς κινούνται οι πελάτες.</p>
          <div class="tags">
            <span class="tag category">κατάστημα</span>
            <span class="tag">Analytics</span>
            <span class="tag">Behavioural</span>
            <span class="tag mode">Counting · Path</span>
            <span class="tag mode">Occupancy</span>
            <span class="tag ok">Spot · Area</span>
          </div>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Διευθυντής καταστήματος (digests κίνησης / occupancy)</li>
            <li>Store ops · shift lead (alerts ζώνης / dwell)</li>
            <li>Regional retail ops (πακέτα multi-site)</li>
            <li>Loss prevention · facilities (επιλεγμένα behavioural events)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>διευθυντής καταστήματος</strong> μπορεί πλέον να δει πώς κινούνται οι πελάτες — μετρήσεις, διαδρομές, heatmaps, dwell και occupancy alerts — στις κάμερες που ήδη υπάρχουν στον όροφο, με digests αντί για cloud footage και video που δεν χρειάζεται να φύγει από τον χώρο.</p>
      </div>
    </article>
"""

CASES["why-cottage-el.html"] = """\
<article class="case-page" id="wedge-family">
      <span id="wedge-family-remote" class="anchor-target" aria-hidden="true"></span>
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/family-protection-home.jpg" alt="EyeNet οικογενειακή προστασία στο σπίτι και εξ αποστάσεως" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 04</span>
          <h2>Ηρεμία στο σπίτι — και μακριά</h2>
          <p class="who">Οικογένειες · γονείς · νοικοκυριά · φοιτητές μακριά από το σπίτι</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Οι οικογένειες χρειάζονται αυτοματοποιημένη προστασία για σπίτι, εξοχικό και φοιτητές μακριά — χωρίς πλήρη ομάδα ασφαλείας ή υποχρεωτικό cloud video. Το EyeNet επιβεβαιώνει παρουσίες και ειδοποιεί όταν άγνωστο πρόσωπο στέκεται μπροστά σε πόρτα ή μπαίνει σε χώρους διαβίωσης. Λαμβάνετε λίγες στοχευμένες ειδοποιήσεις τηλεφώνου· το υλικό μένει τοπικά.</p>
          <ul class="case-features">
            <li><strong>Προστασία σπιτιού</strong> — alerts εισβολής και αγνώστων όταν το σπίτι είναι κενό</li>
            <li><strong>Οικογένεια μακριά / φοιτητές</strong> — ηρεμία όταν αγαπημένα πρόσωπα ζουν μακριά, χωρίς cloud video</li>
            <li><strong>Έλεγχος παρουσίας</strong> — επιβεβαίωση ότι κάποιος είναι (ή πρέπει να είναι) στο σπίτι</li>
            <li><strong>Secure zones</strong> — συναγερμός αν άγνωστο πρόσωπο σταθεί μπροστά σε πόρτα ή μπει σε χώρους διαβίωσης</li>
            <li><strong>On-prem ιδιωτικότητα</strong> — το υλικό μένει τοπικά· ειδοποιήσεις τηλεφώνου μόνο όταν χρειάζεται</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Προστασία της οικογένειας στο σπίτι και όταν κάποιος είναι μακριά — αυτόματα, ιδιωτικά, χωρίς πλήρη ομάδα ασφαλείας.</p>
          <div class="tags">
            <span class="tag category">σπίτι</span>
            <span class="tag">Gate</span>
            <span class="tag">Presence</span>
            <span class="tag">Automation</span>
            <span class="tag mode">Spot · Area</span>
          </div>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Γονείς / οικογένεια (mobile push · email)</li>
            <li>Κάτοικος (φοιτητής / μέλος νοικοκυριού)</li>
            <li>Φροντιστής / γείτονας (προαιρετικά)</li>
            <li>Τοπική επαφή απόκρισης (μόνο κριτικά)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>γονέας</strong> μπορεί πλέον να μετατρέψει μια κάμερα πόρτας σε έξυπνο κουδούνι — alerts για γνωστά και άγνωστα πρόσωπα, plus webhooks σε smart-home οθόνες και ήχο — στις κάμερες που ήδη έχει ή σε φθηνή καθημερινή κάμερα, χωρίς cloud συνδρομή. Προεπιλογή μόνο alerts με τοπικό υλικό· live view μόνο όταν συμφωνούν όλοι οι εμπλεκόμενοι.</p>
        <p class="case-buyer alt">Ένας <strong>γονέας φοιτητή μακριά από το σπίτι</strong> μπορεί πλέον να «βλέπει» απομακρυσμένο διαμέρισμα ή εξοχικό με μία συνηθισμένη κάμερα — μόνο ειδοποιήσεις τηλεφώνου, χωρίς συμβόλαιο φύλαξης ή cloud VMS. Οι ενδιαφερόμενοι παίρνουν το ping χωρίς να φύγει video εκτός χώρου, και μπορούν να ανοίξουν live stream μόνο αν συμφωνούν όλα τα μέρη.</p>
      </div>
    </article>
"""

CASES["why-home-care-el.html"] = """\
<article class="case-page" id="wedge-care">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/homecare-caregiver-presence.jpg" alt="Talos Homecare — παρουσία φροντιστή" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: talosgroup.eu/solutions/integration/homecare</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 05</span>
          <h2>Νοσοκομειακή φροντίδα στο σπίτι</h2>
          <p class="who">Πάροχος φροντίδας · κλινικός MDT · ασθενής / οικογένεια · συνεργάτης Talos / TMAIX eHealth</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Το EyeNet μετατρέπει το σπίτι χωρίς προσωπικό σε περιβάλλον φροντίδας που εμπιστεύονται MDT και φροντιστές. Πτώσεις, κλήσεις βοήθειας, παρουσία και παραβιάσεις ζωνών γίνονται λίγες στοχευμένες ειδοποιήσεις στο clinical stack — το video μένει στον χώρο τοπικά. Συνεργάτες όπως Talos / TMAIX ενώνουν αυτά τα γεγονότα σε ροές Virtual Ward χωρίς cloud footage.</p>
          <ul class="case-features">
            <li><strong>Παρουσία φροντιστή</strong> — σωστό προσωπικό, σωστό σπίτι, σωστή ώρα (διασφάλιση επίσκεψης)</li>
            <li><strong>Secure zones</strong> — συναγερμός για άγνωστα πρόσωπα μέσα/γύρω από την κατοικία</li>
            <li><strong>Ανίχνευση πτώσης</strong> — αυτόματη άμεση ειδοποίηση σε ομάδα φροντίδας και οικεία πρόσωπα</li>
            <li><strong>Φωνή / κλήση βοήθειας</strong> — προφορικό αίτημα βοήθειας → άμεσα ενεργή ειδοποίηση</li>
            <li><strong>Ενημέρωση συστημάτων υγείας</strong> — tokenized γεγονότα σε ePokratis / IoMT / telemedicine (όχι cloud video)</li>
            <li><strong>Virtual Ward</strong> — φροντίδα επιπέδου νοσοκομείου στο σπίτι: αποφυγή εισαγωγής &amp; πρώιμη έξοδος</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Διαφοροποίηση έναντι vitals-only RPM: το σπίτι γίνεται περιβάλλον παρακολουθούμενης φροντίδας. Ιδιωτικότητα by architecture — η όραση μένει on-prem· μόνο γεγονότα πτώσης / βοήθειας / παρουσίας / ζώνης φτάνουν στο health stack.</p>
          <div class="tags">
            <span class="tag category">σπίτι</span>
            <span class="tag category">φροντίδα</span>
            <span class="tag">Presence</span>
            <span class="tag">Automation</span>
            <span class="tag safety">Fall</span>
            <span class="tag safety">Voice</span>
            <span class="tag mode">Area · Spot</span>
            <span class="tag user">Talos · TMAIX</span>
          </div>
          <p class="side-note"><strong>Συνεργάτης:</strong> Talos eHealth / IoMT · TMAIX ePpocrates eCloud</p>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>MDT / συντονιστής φροντίδας · εφημερεύων κλινικός</li>
            <li>Ορισμένος φροντιστής (mobile)</li>
            <li>Οικογένεια / χορηγός ασθενούς (επιλεγμένα γεγονότα)</li>
            <li>Ουρά telemedicine / ePokratis</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>πάροχος φροντίδας</strong> μπορεί πλέον να μετατρέψει μια κάμερα δωματίου ασθενούς σε γεγονότα πτώσης και κλήσης βοήθειας για το clinical stack — με alerts σε όλους τους ενδιαφερόμενους, φροντιστές και οικεία πρόσωπα, κλιμακούμενα ανά ρυθμίσεις — χωρίς cloud video. Τα οικεία πρόσωπα μένουν ήσυχα χωρίς να είναι κολλημένα στην κάμερα: παίρνουν άμεσα alerts, πλήρη εικόνα για το ποιος είναι στον χώρο και αν οι φροντιστές είναι εκεί και στην ώρα τους, με live feed διαθέσιμο ανά πάσα στιγμή.</p>
      </div>
    </article>
"""

CASES["why-security-el.html"] = """\
<article class="case-page" id="wedge-security">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/security.jpg" alt="EyeNet παρακολούθηση ασφαλείας" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 06</span>
          <h2>Νυχτερινές βάρδιες που επαγρυπνούν</h2>
          <p class="who">Εταιρείες ασφαλείας · εταιρική / βιομηχανική / κυβερνητική φύλαξη</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Η νυχτερινή και περιμετρική κάλυψη δεν μπορεί να βασίζεται στην ελπίδα ότι κάθε πόστο μένει ξύπνιο. Το EyeNet παρακολουθεί σταθμούς και περίμετρο συνεχώς και κλιμακώνει όταν ένα πόστο σιωπά ή εμφανίζεται κίνηση. Η συνεχής εγγραφή είναι έτοιμη ώστε τα περιστατικά να έχουν χρονοσημασμένα αποδεικτικά.</p>
          <ul class="case-features">
            <li><strong>Αυτοματοποίηση νυχτερινής βάρδιας</strong> — αυτοματοποιημένη παρακολούθηση ότι οι φύλακες μένουν ξύπνιοι και σε εγρήγορση</li>
            <li><strong>Presence σε θέσεις</strong> — υπηρεσίες Presence σε φυλάκια καθ’ όλη τη βάρδια</li>
            <li><strong>Κόμβοι περιμέτρου</strong> — Presence nodes σε φράχτες, πύλες και εξωτερικούς δακτυλίους</li>
            <li><strong>Vradar</strong> — ανίχνευση κίνησης, POI / people-match alerts σε feeds περιπολίας</li>
            <li><strong>Forensics</strong> — συνεχής εγγραφή με χρονοσημασμένα τεκμήρια για συμβάντα</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Η νυχτερινή κάλυψη σταματά να εξαρτάται από την ελπίδα. Αυτόματη κλιμάκωση όταν μια θέση σωπαίνει· περίμετρος + Vradar πιάνουν κίνηση πριν γίνει παραβίαση.</p>
          <div class="tags">
            <span class="tag category">ασφάλεια</span>
            <span class="tag">Presence</span>
            <span class="tag">Sentinel</span>
            <span class="tag safety">Vradar</span>
            <span class="tag mode">Perimeter</span>
            <span class="tag ok">Recording · forensics</span>
          </div>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Φύλακας υπηρεσίας (mobile / συναγερμός θέσης)</li>
            <li>Επόπτης βάρδιας · SOC</li>
            <li>Διευθυντής ασφαλείας χώρου</li>
            <li>Ομάδα απόκρισης · εγκαταστάσεις πελάτη (κριτικά)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>υπεύθυνος λειτουργιών ασφαλείας</strong> μπορεί πλέον να έχει νυχτερινή επαγρύπνηση και περίμετρο από τις κάμερες φράχτη και ορόφου που ήδη υπάρχουν — χωρίς θέσεις ανά κάμερα ή άλλη νυχτερινή βάρδια.</p>
      </div>
    </article>
"""

CASES["why-shipping-el.html"] = """\
<article class="case-page" id="wedge-shipping">
      <div class="case-hero">
        <img loading="lazy" decoding="async" src="/assets/images/shipping.jpg" alt="EyeNet ναυτιλία και βιομηχανία" />
        <div class="case-hero-veil"></div>
        <p class="case-hero-credit">Οπτικό: eyenet-vision.com</p>
        <div class="case-hero-meta">
          <span class="case-hero-num">Περίπτωση 07</span>
          <h2>Ποιος είναι στην θέση του. Ποιος στον χώρο. Ποιος έπεσε.</h2>
          <p class="who">Πλοίαρχος · διαχειριστής στόλου · HQ ξηράς · λειτουργίες εργοστασίου / χώρου · βιομηχανική ασφάλεια</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">Πλοία και βιομηχανικοί χώροι δεν μπορούν να στηριχθούν σε cloud VMS όταν η συνδεσιμότητα είναι ελλειπής ή offline. Το EyeNet κρατά τοπική αλήθεια για το ποιος είναι onboard ή on site και πού πρέπει να είναι, και στέλνει πακέτα αναφορών στην ξηρά ή το HQ. Το ίδιο stack καλύπτει ειδικές ζώνες που χρειάζονται ανίχνευση πτώσης — καταστρώματα, αμπάρια, αποθήκες και βιομηχανικοί όροφοι — ώστε η πτώση να γίνει άμεσο alert, όχι χαμένη κλήση ασυρμάτου.</p>
          <ul class="case-features">
            <li><strong>Ζώνες βιομηχανικού χώρου</strong> — περιορισμένες περιοχές, αυλές και γραμμές παραγωγής ειδοποιούν όταν μπαίνουν λάθος άτομα</li>
            <li><strong>Ανίχνευση πτώσης σε ειδικές περιοχές</strong> — καταστρώματα, αμπάρια, αποθήκες και βιομηχανικοί όροφοι στέλνουν fall alerts στη γέφυρα, την ξηρά ή τις λειτουργίες χώρου</li>
            <li><strong>Παρουσία βάρδιας &amp; εργολάβων</strong> — ποιος είναι στον χώρο σε βάρδιες, εργολάβους και επισκέπτες χωρίς κυνήγι badges</li>
            <li><strong>Alerts κινδύνου / PPE</strong> — προαιρετικά triggers γύρω από υψηλού κινδύνου ζώνες και σημεία συγκέντρωσης σε βιομηχανικά campuses</li>
            <li><strong>Όλοι στη θέση τους στη θάλασσα</strong> — Presence / Gate / Sentinel διασφαλίζουν ότι το πλήρωμα είναι όπου πρέπει</li>
            <li><strong>Ακριβής αριθμός επί του σκάφους</strong> — γνωρίζετε ακριβώς πόσοι είναι onboard ανά πάσα στιγμή</li>
            <li><strong>Αναφορές ξηράς &amp; HQ anytime</strong> — αυτοματοποιημένα πακέτα παρουσίας &amp; headcount στο fleet HQ ή στον έλεγχο εργοστασίου</li>
            <li><strong>Ελάχιστη συνδεσιμότητα</strong> — πλήρης τοπική λειτουργία στη θάλασσα ή σε απομακρυσμένους βιομηχανικούς χώρους· συγχρονισμός σε λεπτούς / διακοπτόμενους συνδέσμους</li>
            <li><strong>Fleet / site Matrix</strong> — VPN mesh· ουρά δεδομένων σε degraded mode — χωρίς απώλεια δεδομένων όταν offline</li>
          </ul>
        </div>
        <aside class="case-aside">
          <h3>Γιατί μετράει</h3>
          <p>Τα πλοία και οι βιομηχανικοί χώροι δεν μπορούν να βασίζονται σε cloud VMS. Το EyeNet δίνει σε πλοίαρχο, ξηρά και λειτουργίες εργοστασίου την ίδια αλήθεια: ποιος είναι onboard ή στον χώρο, πού βρίσκεται — και ανίχνευση πτώσης στις ζώνες που τη χρειάζονται — με αναφορές που ταξιδεύουν σε ελάχιστο bandwidth.</p>
          <div class="tags">
            <span class="tag category">ναυτιλία</span>
            <span class="tag category">βιομηχανία</span>
            <span class="tag">Presence</span>
            <span class="tag">Gate</span>
            <span class="tag">Sentinel</span>
            <span class="tag safety">Fall</span>
            <span class="tag">Matrix</span>
            <span class="tag mode">Offline · VPN</span>
          </div>
          <div class="case-notify">
          <h5>Αυτοματοποιημένες ειδοποιήσεις</h5>
          <ul>
            <li>Πλοίαρχος · γέφυρα / αξιωματικός υπηρεσίας</li>
            <li>Ύπαρχος · αξιωματικός ασφαλείας (επί του σκάφους)</li>
            <li>Λειτουργίες στόλου ξηράς · CSO · επόπτης εργοστασίου / χώρου (συμπ. fall alerts)</li>
            <li>Fleet / site HR (πακέτα παρουσίας / συμμόρφωσης)</li>
          </ul>
        </div>
        </aside>
      </div>
      <div class="case-buyers">
        <p class="case-buyer">Ένας <strong>πλοίαρχος ή υπεύθυνος λειτουργιών εργοστασίου</strong> μπορεί πλέον να ξέρει ποιος είναι onboard και ποιος στη ζώνη όταν πέφτει ο σύνδεσμος — στις κάμερες που ήδη υπάρχουν στο πλοίο ή στον χώρο. Τα HQ παίρνουν real-time alerts ανά ρυθμίσεις plus πλήρη insights και analytics, κλιμακούμενα από έναν χώρο σε ολόκληρα πλοία, στόλους ή βιομηχανικές περιοχές, με recordings και live feed διαθέσιμα.</p>
      </div>
    </article>
"""


def main() -> None:
    for name, body in CASES.items():
        path = CONTENT / name
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
