#!/usr/bin/env python3
"""Generate EyeNet marketing hub + use-case microsites under marketing/web/."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # marketing/web

LOGO_SVG = '''<svg class="header-logo" viewBox="5 5 285 70" xmlns="http://www.w3.org/2000/svg" aria-label="Eyenet">
<rect x="10" y="10" width="8" height="60" fill="#0891b2"/><rect x="18" y="10" width="25" height="8" fill="#0891b2" opacity="0.9"/><rect x="18" y="36" width="20" height="8" fill="#0891b2" opacity="0.8"/><rect x="18" y="62" width="25" height="8" fill="#0891b2"/><rect x="55" y="10" width="8" height="25" fill="#22d3ee"/><rect x="63" y="35" width="8" height="35" fill="#22d3ee" opacity="0.9"/><rect x="71" y="10" width="8" height="25" fill="#22d3ee" opacity="0.8"/><rect x="95" y="10" width="8" height="60" fill="#06b6d4"/><rect x="103" y="10" width="25" height="8" fill="#06b6d4" opacity="0.9"/><rect x="103" y="36" width="20" height="8" fill="#06b6d4" opacity="0.8"/><rect x="103" y="62" width="25" height="8" fill="#06b6d4"/><rect x="145" y="10" width="8" height="60" fill="#0891b2"/><rect x="153" y="20" width="8" height="13" fill="#0891b2" opacity="0.9"/><rect x="161" y="33" width="8" height="14" fill="#0891b2" opacity="0.8"/><rect x="169" y="47" width="8" height="13" fill="#0891b2" opacity="0.9"/><rect x="177" y="10" width="8" height="60" fill="#0891b2"/><rect x="200" y="10" width="8" height="60" fill="#22d3ee"/><rect x="208" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/><rect x="208" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/><rect x="208" y="62" width="25" height="8" fill="#22d3ee"/><rect x="250" y="10" width="30" height="8" fill="#06b6d4"/><rect x="261" y="18" width="8" height="52" fill="#06b6d4" opacity="0.9"/>
</svg>'''

FOOTER_LOGO = LOGO_SVG.replace('class="header-logo"', 'style="max-width:500px;width:100%"').replace(' aria-label="Eyenet"', '')

CASES = [
    {
        "slug": "hr-presence",
        "nav": "Presence",
        "title": "Know who is present and who is not",
        "hero_html": "Know who is <em>present</em> — and who is not",
        "tease": "One flexible Presence tool from doorbell to fleet post.",
        "hero_img": "cases/hr-presence.png",
        "who": "Home · office · warehouse · industrial · shipping · security",
        "value_path": "/why/hr-presence/",
        "quote": "Stop chasing roll-calls. See who is in — automatically.",
        "wedge": {
            "label": "Presence",
            "headline": "Presence is one flexible tool — from <em>doorbell to deck</em>",
            "image": "cases/hr-presence.png",
            "stats": [("∞", "Sites"), ("Auto", "Check-in"), ("0", "Roll-calls")],
            "features": [
                ("Any Premise", "Home, office, warehouse, industrial floor, ship, or security post — same Presence stack."),
                ("Who / Where / When", "EyeNet shows presence automatically so teams stop chasing badges and spreadsheets."),
                ("CRM Aligned", "HubSpot keeps grants and contacts synced as people move across sites."),
            ],
            "chips": "Presence,Handshake,Nod,VProfiles,Matrix",
        },
        "cards": [
            {
                "label": "Home",
                "headline": "Intelligent doorbell that <em>knows who arrived</em>",
                "image": "cases/family-protection-home.jpg",
                "stats": [("Local", "Video"), ("Phone", "Alerts"), ("No", "Cloud footage")],
                "features": [
                    ("Door Presence", "Know who is at the door without shipping video to the cloud."),
                    ("Family Signal", "Targeted alerts when presence matters — not a 24/7 feed to babysit."),
                    ("Same Stack", "The home node uses the same Presence engine as the enterprise floor."),
                ],
                "chips": "Presence,VProfiles",
                "cta": "See home protection",
                "cta_href": "#card-hands-off",
            },
            {
                "label": "Stations",
                "headline": "Entrance and exit stations that <em>check people in</em>",
                "image": "access.png",
                "stats": [("Gate", "Ready"), ("Sub 1s", "Verify"), ("∞", "Doors")],
                "features": [
                    ("Check-in / Out", "Presence stations at doors for automatic entrance and exit tracking."),
                    ("Vprofile Cameras", "Offices, warehouses, industrial floors, and watch posts covered."),
                    ("Desk & Phone", "Staff Presence apps on mobile phones and desk PCs complete the mesh."),
                ],
                "chips": "Presence,Handshake,Nod,VProfiles",
                "cta": "See hands-off ops",
                "cta_href": "#card-hands-off",
            },
            {
                "id": "card-hands-off",
                "label": "Ops",
                "headline": "Hands-off ops — <em>no manual chase</em>",
                "image": "images/eyenet-executive.jpg",
                "stats": [("0", "Spreadsheets"), ("Live", "Grants"), ("HubSpot", "Sync")],
                "features": [
                    ("Pure Automation", "No manual roll-call. Presence writes the truth as people move."),
                    ("Shipping & Security", "Same stack for crew, shifts, and perimeter stations."),
                    ("HubSpot CRM", "First CRM connector: sync contacts and post grants in real time."),
                ],
                "chips": "Presence,Matrix,Insights",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
        ],
        "screenshots": [
            ("screenshots/main-dashboard.png", "Main Dashboard", "Central presence control"),
            ("screenshots/camera-list.png", "Camera List", "Presence cameras across sites"),
            ("screenshots/triggers-list.png", "Triggers", "Presence automation rules"),
            ("screenshots/analytics-01.png", "Analytics", "Presence and attendance insights"),
            ("screenshots/multi-camera-streams.png", "Multi-Camera", "Live presence feeds"),
        ],
        "roles": [
            ("Business Owners & Executives", "images/eyenet-executive.jpg", "Oversight without badge theatre — compliance-ready presence across every site."),
            ("Operations Managers", "images/eyenet-industrial.jpg", "Automatic who/where/when so floors, warehouses, and offices run on truth."),
            ("Security Leads", "images/eyenet-security.jpg", "Watch posts and perimeter stations on the same Presence mesh."),
        ],
        "apps": [
            ("Presence", "Attendance and access monitoring with automated reporting across rooms, gates, and sites.", "Access Control", "Area · Gate"),
            ("Matrix", "Aggregated presence reporting across installations over VPN — fleets and multi-site networks.", "Enterprise", "All Modes"),
        ],
        "modes": ["Spot Mode", "Gate Mode", "Area Mode"],
        "deep": {
            "app": "Presence",
            "blurb": "One Presence tool that stretches from an intelligent doorbell to maritime and industrial posts. EyeNet shows who is in, where, and when — automatically — and keeps CRM grants aligned.",
            "features": [
                ("Intelligent doorbell", "Who is at the door at home; presence without cloud video."),
                ("Entrance / exit stations", "Presence stations at doors for check-in / check-out."),
                ("Vprofile cameras", "Offices, warehouses, industrial floors, and watch posts."),
                ("Presence apps", "Staff mobile phones and desk PCs."),
                ("HubSpot CRM", "Sync contacts and post grants in real time."),
            ],
            "users": "Homes, corporate offices, warehouses, industrial facilities, maritime operators, and security firms.",
            "modes": "Area, Gate, Spot",
        },
    },
    {
        "slug": "mall",
        "nav": "Signage",
        "title": "Screens that sell themselves",
        "hero_html": "Screens that <em>sell themselves</em>",
        "tease": "Audience signals drive playlists. Prove every impression.",
        "hero_img": "cases/mall-signage.png",
        "who": "Retail · venues · agencies · brand studios · digital signage operators",
        "value_path": "/why/mall/",
        "quote": "Static screens burn budget. Live audiences buy.",
        "wedge": {
            "label": "Signage",
            "headline": "Turn every display into a <em>measurable marketing studio</em>",
            "image": "cases/mall-signage.png",
            "stats": [("Sub 1s", "Switch"), ("∞", "Displays"), ("100%", "Measurable")],
            "features": [
                ("Read the Room", "Age, gender, group size — playlist switches in milliseconds."),
                ("Zero Surveys", "Know who saw each display: views, dwell, engagement."),
                ("Prove ROI", "Impression reports and footfall-to-sales funnels — not guesswork."),
            ],
            "chips": "Signage,AnonTracking,Insights",
        },
        "cards": [
            {
                "label": "Audience",
                "headline": "Read the room — then <em>rewrite the playlist</em>",
                "image": "signage.png",
                "stats": [("Live", "Demographics"), ("ms", "Latency"), ("Auto", "Trigger")],
                "features": [
                    ("Audience Signals", "Cameras read who is watching and drive content instantly."),
                    ("Auto-Trigger", "Promotions or emergency messages fire from live presence."),
                    ("Any Spot", "Concourses, shops, gates — every screen becomes a studio surface."),
                ],
                "chips": "Signage,AnonTracking",
                "cta": "Measure what converts",
                "cta_href": "#card-roi",
            },
            {
                "id": "card-roi",
                "label": "ROI",
                "headline": "A/B in the wild — <em>prove what converts</em>",
                "image": "images/eyenet-marketing-02.jpg",
                "stats": [("A/B", "Live"), ("Zero", "Surveys"), ("Full", "Funnel")],
                "features": [
                    ("Wild Testing", "Swap content on live audience data and measure conversion."),
                    ("Engagement Rates", "Views, dwell, and attention without clipboard surveys."),
                    ("Sales Funnel", "Footfall-to-sales reporting that marketing can defend."),
                ],
                "chips": "Signage,Insights",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
            {
                "label": "Deploy",
                "headline": "Everyday hardware. <em>Studio-grade</em> outcomes.",
                "image": "instant.png",
                "stats": [("16 GB", "RAM"), ("Sub 5min", "Setup"), ("On-Prem", "Private")],
                "features": [
                    ("Plug & Play", "Connect existing cameras and displays — first detection in minutes."),
                    ("On-Prem", "Audience intelligence stays local; no cloud video dependency."),
                    ("Scale Spots", "Start with one screen; expand across the mall or network."),
                ],
                "chips": "Signage,Insights,VProfiles",
                "cta": "Explore modes",
                "cta_href": "#operating-modes",
            },
        ],
        "screenshots": [
            ("screenshots/digital-signage-01.png", "Digital Signage", "Playlist and media control"),
            ("screenshots/analytics-01.png", "Analytics", "Audience and engagement"),
            ("screenshots/anaytics-filters.png", "Filters", "Slice by time and zone"),
            ("screenshots/main-dashboard.png", "Dashboard", "Campaign oversight"),
            ("screenshots/actions-edit.png", "Actions", "Trigger playlists from vision"),
        ],
        "roles": [
            ("Marketing & Sales Teams", "images/eyenet-marketing-02.jpg", "Serve the right creative to the right audience and prove campaign ROI."),
            ("Retail Operators", "images/eyenet-executive.jpg", "Turn concourses and shop spots into measurable marketing surfaces."),
            ("Agency Studios", "cases/mall-signage.png", "Run A/B tests in the wild with live demographic feedback."),
        ],
        "apps": [
            ("Signage", "Demographic-driven content delivery with real-time audience analytics for retail and venues.", "Retail & Marketing", "Spot · Gate · Area"),
        ],
        "modes": ["Spot Mode", "Gate Mode", "Area Mode"],
        "deep": {
            "app": "Signage",
            "blurb": "Static screens burn budget because nobody can prove who saw what. EyeNet reads the room and drives playlists from live audience signals — views, dwell, and engagement as a measurable marketing studio.",
            "features": [
                ("Read the room", "Age, gender, group size drive playlist switches in milliseconds."),
                ("Zero surveys", "Know who sees each display: views, dwell, engagement."),
                ("A/B in the wild", "Swap content on live audience data; measure what converts."),
                ("Prove ROI", "Impression reports, engagement rates, footfall-to-sales funnels."),
            ],
            "users": "Retail shops, shopping malls, airports, advertising agencies, event venues, and marketing firms.",
            "modes": "Spot, Gate, Area",
        },
    },
    {
        "slug": "shop-floor",
        "nav": "Shop Floor",
        "title": "See how shoppers move",
        "hero_html": "See how shoppers <em>move</em>",
        "tease": "Counts, paths, heatmaps, dwell — video stays in-store.",
        "hero_img": "cases/shop-floor.jpg",
        "who": "Shop managers · store ops · multi-site retail",
        "value_path": "/why/shop-floor/",
        "quote": "Traffic is not insight. Movement is.",
        "wedge": {
            "label": "Retail Ops",
            "headline": "Turn cameras into <em>movement intelligence</em>",
            "image": "cases/shop-floor.jpg",
            "stats": [("Live", "Counts"), ("Path", "Heatmaps"), ("On-Prem", "Video")],
            "features": [
                ("People Counting", "Face / body / both across entrances and floor cameras."),
                ("Paths & Heatmaps", "See how customers move through aisles and zones."),
                ("Behavioural Alerts", "Occupancy, dwell, path, and co-presence → mobile, email, webhook."),
            ],
            "chips": "Insights,AnonTracking,Presence,Gate",
        },
        "cards": [
            {
                "label": "Flow",
                "headline": "Paths, peaks, and dwell — <em>not just footfall</em>",
                "image": "images/eyenet-industrial.jpg",
                "stats": [("Busy", "Hours"), ("Zone", "Occupancy"), ("Dwell", "Patterns")],
                "features": [
                    ("Occupancy & Peaks", "Busy hours by area — not guesswork from the till."),
                    ("Visit Patterns", "Where shoppers linger versus pass through."),
                    ("Manager Digests", "Ops get digests and alerts; video never has to leave the store."),
                ],
                "chips": "Insights,AnonTracking",
                "cta": "See behavioural alerts",
                "cta_href": "#card-alerts",
            },
            {
                "id": "card-alerts",
                "label": "Alerts",
                "headline": "Behavioural alerts when zones get <em>too busy — or too quiet</em>",
                "image": "restricted.png",
                "stats": [("Mobile", "Push"), ("Email", "Digest"), ("Webhook", "Ready")],
                "features": [
                    ("Zone Triggers", "Occupancy / dwell / path / co-presence fire operational actions."),
                    ("Multi-Site", "Same playbook across stores without cloud video."),
                    ("Privacy First", "On-prem processing; managers see signals, not a public stream."),
                ],
                "chips": "Insights,Presence,Logic",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
            {
                "label": "Privacy",
                "headline": "Store truth stays <em>in the store</em>",
                "image": "remote.jpg",
                "stats": [("Zero", "Cloud video"), ("VPN", "Optional"), ("Audit", "Ready")],
                "features": [
                    ("Local Footage", "Video stays on premises by design."),
                    ("Ops-Ready Logs", "Timestamped occupancy and incident records when needed."),
                    ("Scale Quietly", "Start with one floor; expand to the chain."),
                ],
                "chips": "Insights,Matrix,Storage",
                "cta": "Explore modes",
                "cta_href": "#operating-modes",
            },
        ],
        "screenshots": [
            ("screenshots/camera-analytics-01.png", "Camera Analytics", "Floor and entrance metrics"),
            ("screenshots/analytics-01.png", "Analytics", "Movement and occupancy"),
            ("screenshots/anaytics-02.png", "Advanced Analytics", "Trends across zones"),
            ("screenshots/triggers-list.png", "Triggers", "Behavioural alert rules"),
            ("screenshots/multi-camera-streams.png", "Multi-Camera", "Floor coverage"),
        ],
        "roles": [
            ("Shop Managers", "cases/shop-floor.jpg", "See how customers move — not only that someone walked in."),
            ("Store Operations", "images/eyenet-industrial.jpg", "Busy-hour planning and zone staffing from live occupancy."),
            ("Multi-Site Retail", "images/eyenet-executive.jpg", "Comparable movement intelligence across the network."),
        ],
        "apps": [
            ("Gate", "People counters, demographics, heatmaps, and crowd behaviour for entrances and corridors.", "Security & Ops", "Gate"),
            ("Insights", "Aggregated people-activity analytics for floors, zones, and campaigns.", "Analytics", "Spot · Gate · Area"),
        ],
        "modes": ["Spot Mode", "Gate Mode", "Area Mode"],
        "deep": {
            "app": "Gate",
            "blurb": "Shop managers need how customers move through the premises — not only that someone entered. EyeNet turns existing cameras into counts, paths, heatmaps, dwell, and occupancy with behavioural alerts. Video stays in-store.",
            "features": [
                ("People counting", "Face / Body / Both across entrances and floor cameras."),
                ("Paths & heatmaps", "How customers move through aisles and zones."),
                ("Occupancy & peaks", "Busy hours by area, not guesswork."),
                ("Behavioural alerts", "Occupancy / dwell / path / co-presence → mobile, email, webhook."),
                ("On-prem privacy", "Video stays local; managers get digests and alerts."),
            ],
            "users": "Shop managers, store operations, and multi-site retail networks.",
            "modes": "Gate, Spot, Area",
        },
    },
    {
        "slug": "cottage",
        "nav": "Home",
        "title": "Peace of mind at home — and away",
        "hero_html": "Peace of mind at home — <em>and away</em>",
        "tease": "Presence and unknown-person alerts. Footage stays local.",
        "hero_img": "cases/family-protection-home.jpg",
        "who": "Families · parents · households · students living away",
        "value_path": "/why/cottage/",
        "quote": "Protection without a security team — or a cloud of your life.",
        "wedge": {
            "label": "Family",
            "headline": "Light protection for home, cottage, and <em>students away</em>",
            "image": "cases/family-protection-home.jpg",
            "stats": [("Local", "Footage"), ("Few", "Alerts"), ("No", "Cloud lock-in")],
            "features": [
                ("Presence Check", "Confirm someone is — or should be — at home."),
                ("Unknown Person", "Alarm when an unspecified person enters living areas."),
                ("Phone First", "A few targeted notifications; footage stays on premises."),
            ],
            "chips": "Presence,VProfiles,Logic",
        },
        "cards": [
            {
                "label": "Home",
                "headline": "Intrusion alerts when the house is <em>empty</em>",
                "image": "cases/remote-cottage.jpg",
                "stats": [("Empty", "Mode"), ("Instant", "Alert"), ("On-Prem", "Private")],
                "features": [
                    ("Home Protection", "Unknown-person alerts without a full security team."),
                    ("Cottage Ready", "Same stack for secondary homes and seasonal places."),
                    ("Everyday Hardware", "Ordinary cameras — intelligent presence."),
                ],
                "chips": "Presence,VProfiles",
                "cta": "Students away",
                "cta_href": "#card-away",
            },
            {
                "id": "card-away",
                "label": "Away",
                "headline": "Loved ones living away — <em>without cloud video</em>",
                "image": "remote.jpg",
                "stats": [("Family", "Notify"), ("Secure", "Zones"), ("Privacy", "First")],
                "features": [
                    ("Remote Students", "Peace of mind when family lives away."),
                    ("Secure Zones", "Living areas that alarm on unspecified presence."),
                    ("On-Prem Privacy", "Footage stays local; phone alerts only when needed."),
                ],
                "chips": "Presence,Logic",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
            {
                "label": "Simple",
                "headline": "Start small. Stay <em>private</em>.",
                "image": "instant.png",
                "stats": [("1", "Camera"), ("Minutes", "Setup"), ("∞", "Scale later")],
                "features": [
                    ("Plug & Play", "First detection runs in minutes on everyday hardware."),
                    ("No Lock-in", "No cloud subscription required for video."),
                    ("Grow Quietly", "Add rooms or a cottage when you are ready."),
                ],
                "chips": "Presence,VProfiles,Insights",
                "cta": "Explore modes",
                "cta_href": "#operating-modes",
            },
        ],
        "screenshots": [
            ("screenshots/single-camera-stream.png", "Live Camera", "Home presence view"),
            ("screenshots/triggers-list.png", "Triggers", "Unknown-person and zone rules"),
            ("screenshots/actions-edit.png", "Actions", "Phone alert automation"),
            ("screenshots/main-dashboard.png", "Dashboard", "Household overview"),
            ("screenshots/soft-camera-01.jpg", "Soft Camera", "Everyday hardware"),
        ],
        "roles": [
            ("Families & Parents", "cases/family-protection-home.jpg", "Know the house is quiet — and get alerted when it is not."),
            ("Households", "cases/remote-cottage.jpg", "Cottage and secondary-home protection without a guard contract."),
            ("Students Away", "images/eyenet-executive.jpg", "Presence reassurance without streaming life to the cloud."),
        ],
        "apps": [
            ("Presence", "Confirm who is home and alert on unspecified persons in living areas.", "Home Protection", "Area · Spot"),
        ],
        "modes": ["Spot Mode", "Area Mode"],
        "deep": {
            "app": "Presence",
            "blurb": "Families need light protection for the home, cottage, and students living away — without a full security team or forced cloud video. EyeNet confirms presence and alerts when an unknown person enters living areas.",
            "features": [
                ("Home protection", "Intrusion and unknown-person alerts when the house is empty."),
                ("Family away / remote students", "Peace of mind without cloud video."),
                ("Presence check", "Confirm someone is (or should be) at home."),
                ("Secure zones", "Alarm if an unspecified person enters living areas."),
                ("On-prem privacy", "Footage stays local; phone alerts only when needed."),
            ],
            "users": "Families, parents, households, and students living away.",
            "modes": "Spot, Area",
        },
    },
    {
        "slug": "home-care",
        "nav": "Home Care",
        "title": "Hospital-grade care at home",
        "hero_html": "Hospital-grade care <em>at home</em>",
        "tease": "Falls, visits, zones — clinical alerts. Video stays on-prem.",
        "hero_img": "cases/homecare-caregiver-presence.jpg",
        "who": "Care provider · MDT clinician · patient / family · Talos / TMAIX eHealth partner",
        "value_path": "/why/home-care/",
        "quote": "The unstaffed home becomes a ward the MDT can trust.",
        "wedge": {
            "label": "Virtual Ward",
            "headline": "Turn the unstaffed home into a <em>care environment</em>",
            "image": "cases/homecare-caregiver-presence.jpg",
            "stats": [("On-Prem", "Video"), ("Clinical", "Alerts"), ("Token", "Events")],
            "features": [
                ("Visit Assurance", "Right caregiver, right home, right time."),
                ("Fall & Help-Call", "Already-developed triggers → care team — not a missed check-in."),
                ("Clinical Fuse", "Tokenized events into ePokratis / IoMT / telemedicine — not cloud video."),
            ],
            "chips": "Presence,Logic,API,Insights",
        },
        "cards": [
            {
                "label": "Presence",
                "headline": "Caregiver presence — <em>visit assurance</em>",
                "image": "cases/homecare-caregiver-presence.jpg",
                "stats": [("Right", "Staff"), ("Right", "Home"), ("Right", "Time")],
                "features": [
                    ("Assigned Visits", "Confirm the caregiver who should be there actually arrived."),
                    ("Family Signal", "Selected events can notify sponsors without exposing footage."),
                    ("MDT Ready", "Presence facts feed coordinators and on-call clinicians."),
                ],
                "chips": "Presence,VProfiles",
                "cta": "Secure the dwelling",
                "cta_href": "#card-zones",
            },
            {
                "id": "card-zones",
                "label": "Zones",
                "headline": "Secure zones around the <em>dwelling</em>",
                "image": "restricted.png",
                "stats": [("Zone", "Breach"), ("Sub 1s", "Alert"), ("24/7", "Watch")],
                "features": [
                    ("Unspecified Persons", "Alarm on unknown presence in or around the home."),
                    ("Targeted Escalation", "A few clinical alerts — not a noise floor of false positives."),
                    ("Evidence Local", "Timestamped context stays on premises."),
                ],
                "chips": "Presence,AnonTracking,Logic",
                "cta": "Fall & help-call",
                "cta_href": "#card-fall",
            },
            {
                "id": "card-fall",
                "label": "Safety",
                "headline": "Fall detection and voice <em>help-calls</em>",
                "image": "security-cap.jpg",
                "stats": [("Fall", "Trigger"), ("Voice", "Help"), ("Care", "Team")],
                "features": [
                    ("Fall Automation", "Developed trigger routes straight to the care team."),
                    ("Spoken Help", "Voice / help-call becomes an immediate actionable alert."),
                    ("Admission Avoidance", "Virtual Ward workflows for early discharge and hospital-level care at home."),
                ],
                "chips": "Logic,API,Presence",
                "cta": "Clinical fuse",
                "cta_href": "#card-fuse",
            },
            {
                "id": "card-fuse",
                "label": "Clinical",
                "headline": "Tokenized events into the <em>clinical stack</em>",
                "image": "remote.jpg",
                "stats": [("No", "Cloud video"), ("Talos", "TMAIX"), ("Virtual", "Ward")],
                "features": [
                    ("eHealth Partners", "Talos / TMAIX fuse events into Virtual Ward workflows."),
                    ("IoMT / Telemedicine", "Events enter ePokratis and care queues — footage does not."),
                    ("Privacy by Design", "Hospital-grade outcomes without shipping home video to the cloud."),
                ],
                "chips": "API,Logic,Presence,Matrix",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
        ],
        "screenshots": [
            ("screenshots/triggers-list.png", "Triggers", "Fall, zone, and presence rules"),
            ("screenshots/actions-edit.png", "Actions", "Care-team alert routing"),
            ("screenshots/single-camera-stream.png", "Live Feed", "On-prem home node"),
            ("screenshots/main-dashboard.png", "Dashboard", "Care overview"),
            ("screenshots/analytics-01.png", "Analytics", "Visit and event history"),
        ],
        "roles": [
            ("Care Providers & MDT", "cases/homecare-caregiver-presence.jpg", "Trust the unstaffed home with a few targeted clinical alerts."),
            ("Patients & Family", "cases/family-protection-home.jpg", "Hospital-level reassurance without cloud footage of private life."),
            ("eHealth Partners", "images/eyenet-executive.jpg", "Fuse tokenized vision events into Virtual Ward and telemedicine stacks."),
        ],
        "apps": [
            ("Presence", "Caregiver visit assurance and dwelling zone protection with on-prem video.", "Care Access", "Area · Spot"),
            ("Logic", "Fall, help-call, and zone automations routed to clinical and family stakeholders.", "Automation", "All Modes"),
        ],
        "modes": ["Spot Mode", "Area Mode"],
        "deep": {
            "app": "Presence",
            "blurb": "EyeNet turns the unstaffed home into a care environment MDT teams and caregivers can trust. Falls, help-calls, presence, and zone breaches become targeted alerts — video stays on-prem. Partners fuse tokenized events into Virtual Ward workflows.",
            "features": [
                ("Caregiver presence", "Right staff, right home, right time (visit assurance)."),
                ("Secure zones", "Alarm on unspecified persons in/around the dwelling."),
                ("Fall detection", "Automation trigger → care team."),
                ("Voice / help-call", "Spoken request for help → immediate actionable alert."),
                ("Clinical fuse", "Tokenized events into ePokratis / IoMT / telemedicine (not cloud video)."),
                ("Virtual Ward", "Admission avoidance and early discharge at home."),
            ],
            "users": "Care providers, MDT clinicians, patients and families, Talos / TMAIX and eHealth partners.",
            "modes": "Spot, Area",
        },
    },
    {
        "slug": "security",
        "nav": "Security",
        "title": "Night shifts that never blink",
        "hero_html": "Night shifts that <em>never blink</em>",
        "tease": "Stations and fences watched continuously. Evidence ready.",
        "hero_img": "cases/security.jpg",
        "who": "Security firms · corporate / industrial / government guard ops",
        "value_path": "/why/security/",
        "quote": "Hope is not a night-shift strategy.",
        "wedge": {
            "label": "Sentinel",
            "headline": "Posts and perimeters that <em>escalate before they fail</em>",
            "image": "cases/security.jpg",
            "stats": [("24/7", "Watch"), ("Quiet", "Post alert"), ("Forensic", "Ready")],
            "features": [
                ("Night Automation", "First-time monitoring that guards stay awake and alert."),
                ("Perimeter Nodes", "Presence at fences, gates, and outer rings."),
                ("Timestamped Evidence", "Continuous recording ready when incidents happen."),
            ],
            "chips": "Sentinel,Presence,VRadar,Insights",
        },
        "cards": [
            {
                "label": "Posts",
                "headline": "Presence at watch stations <em>across the shift</em>",
                "image": "security-cap.jpg",
                "stats": [("Post", "Presence"), ("Inactivity", "Alert"), ("Live", "Annotate")],
                "features": [
                    ("Station Watch", "Presence services on every watch post."),
                    ("Quiet Escalation", "Escalate when a post goes quiet."),
                    ("Shift Proof", "Operators see verified alerts — not every raw feed."),
                ],
                "chips": "Sentinel,Presence",
                "cta": "Perimeter",
                "cta_href": "#card-perimeter",
            },
            {
                "id": "card-perimeter",
                "label": "Perimeter",
                "headline": "Fences and outer rings that <em>never sleep</em>",
                "image": "restricted.png",
                "stats": [("Fence", "Nodes"), ("Motion", "Hit"), ("POI", "Match")],
                "features": [
                    ("Perimeter Presence", "Nodes at fences, gates, and outer rings."),
                    ("Vradar", "Motion detection and POI / people-match on patrol feeds."),
                    ("Multi-Cam", "Coordinate the ring from one command view."),
                ],
                "chips": "Presence,VRadar,AnonTracking",
                "cta": "Forensics",
                "cta_href": "#card-forensics",
            },
            {
                "id": "card-forensics",
                "label": "Forensics",
                "headline": "Incidents with <em>timestamped evidence</em> — not guesswork",
                "image": "vip.png",
                "stats": [("Continuous", "Record"), ("Audit", "Ready"), ("Export", "Fast")],
                "features": [
                    ("Always Recording", "Evidence ready when the night goes wrong."),
                    ("Shift Handover", "Timelines and exports for the next team."),
                    ("On-Prem Secure", "Footage stays where policy demands."),
                ],
                "chips": "Sentinel,Insights,Storage",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
        ],
        "screenshots": [
            ("screenshots/multi-camera-streams.png", "Multi-Camera", "Posts and perimeter feeds"),
            ("screenshots/triggers-list.png", "Triggers", "Inactivity and motion rules"),
            ("screenshots/actions-edit.png", "Actions", "Escalation playbooks"),
            ("screenshots/camera-analytics-02.png", "Camera Stats", "Night coverage metrics"),
            ("screenshots/main-dashboard.png", "Dashboard", "Command overview"),
        ],
        "roles": [
            ("Security Firms", "cases/security.jpg", "Multiply the night team with always-on station and fence watch."),
            ("Corporate & Industrial Guard Ops", "images/eyenet-security.jpg", "Escalate quiet posts and perimeter hits before they become incidents."),
            ("Government Sites", "images/eyenet-executive.jpg", "Audit-ready evidence with on-prem control."),
        ],
        "apps": [
            ("Sentinel", "Automated personnel monitoring at watch stations with activity / inactivity alerts.", "Personnel Monitoring", "Area"),
            ("VRadar", "Mobile and patrol feeds with POI alerts and central command integration.", "Mobile Security", "Goggles · Drone"),
        ],
        "modes": ["Area Mode", "Gate Mode", "Goggles Mode"],
        "deep": {
            "app": "Sentinel",
            "blurb": "Night and perimeter coverage cannot depend on hope that every post stays awake. EyeNet watches stations and fences continuously and escalates when a post goes quiet or motion hits the ring — with timestamped evidence ready.",
            "features": [
                ("Night-shift automation", "Monitoring that guards stay awake and alert."),
                ("Presence at posts", "Presence services on watch stations across the shift."),
                ("Perimeter nodes", "Presence nodes at fences, gates, and outer rings."),
                ("Vradar", "Motion detection, POI / people-match alerts on patrol feeds."),
                ("Forensics", "Continuous recording with timestamped evidence."),
            ],
            "users": "Security firms and corporate, industrial, and government guard operations.",
            "modes": "Area, Gate, Goggles",
        },
    },
    {
        "slug": "shipping",
        "nav": "Shipping",
        "title": "Who’s onboard. Who’s on site. Who fell.",
        "hero_html": "Who’s onboard. Who’s on site. <em>Who fell.</em>",
        "tease": "Local truth at sea and on industrial sites — reports to shore.",
        "hero_img": "cases/shipping.jpg",
        "who": "Captain · fleet manager · shore HQ · plant / site ops · industrial security",
        "value_path": "/why/shipping/",
        "quote": "Thin links. Full local truth. Shore reports when you can.",
        "wedge": {
            "label": "Fleet & Site",
            "headline": "Onboard and on-site truth when the <em>cloud cannot reach</em>",
            "image": "cases/shipping.jpg",
            "stats": [("Local", "Ops"), ("Exact", "Headcount"), ("Fall", "Alert")],
            "features": [
                ("Who Is Where", "Crew and site presence without badge chasing over thin links."),
                ("Fall Zones", "Decks, holds, warehouses, and industrial floors trigger immediately."),
                ("Shore / HQ Packs", "Attendance and headcount reports when connectivity allows."),
            ],
            "chips": "Presence,Gate,Sentinel,Matrix",
        },
        "cards": [
            {
                "label": "Zones",
                "headline": "Industrial zones that alert when the <em>wrong people enter</em>",
                "image": "restricted.png",
                "stats": [("Yard", "Floor"), ("Restricted", "Zones"), ("Live", "Alert")],
                "features": [
                    ("Site Zones", "Restricted areas, yards, and production floors."),
                    ("Shift & Contractors", "Know who is on site across shifts, contractors, and visitors."),
                    ("Hazard Optional", "Triggers around high-risk zones and muster points."),
                ],
                "chips": "Presence,Gate,Insights",
                "cta": "Fall detection",
                "cta_href": "#card-fall-ship",
            },
            {
                "id": "card-fall-ship",
                "label": "Safety",
                "headline": "Fall detection where radio calls <em>get missed</em>",
                "image": "security-cap.jpg",
                "stats": [("Deck", "Hold"), ("Warehouse", "Floor"), ("Bridge", "Alert")],
                "features": [
                    ("Special Areas", "Decks, holds, warehouses, and industrial floors."),
                    ("Immediate Route", "Fall alerts to bridge, shore, or site ops."),
                    ("Everyone in Place", "Presence / Gate / Sentinel keep crew where they should be."),
                ],
                "chips": "Logic,Presence,Sentinel",
                "cta": "Shore reports",
                "cta_href": "#card-shore",
            },
            {
                "id": "card-shore",
                "label": "Shore",
                "headline": "Exact onboard count — <em>reports to HQ anytime</em>",
                "image": "remote.jpg",
                "stats": [("Exact", "Count"), ("Thin", "Link sync"), ("Matrix", "Mesh")],
                "features": [
                    ("Headcount Truth", "Know precisely how many people are onboard or on site."),
                    ("Minimal Connectivity", "Full local ops; sync over intermittent links."),
                    ("Fleet Matrix", "VPN mesh with degraded mode — no data loss when offline."),
                ],
                "chips": "Matrix,Presence,Insights",
                "cta": "See it in action",
                "cta_href": "#in-action",
            },
        ],
        "screenshots": [
            ("screenshots/multi-camera-streams.png", "Multi-Camera", "Deck and site coverage"),
            ("screenshots/camera-list.png", "Cameras", "Installation inventory"),
            ("screenshots/analytics-01.png", "Analytics", "Presence and headcount"),
            ("screenshots/triggers-list.png", "Triggers", "Fall and zone rules"),
            ("screenshots/main-dashboard.png", "Dashboard", "Fleet / site overview"),
        ],
        "roles": [
            ("Captains & Fleet Managers", "cases/shipping.jpg", "Exact onboard truth with fall alerts that reach the bridge."),
            ("Shore HQ", "images/eyenet-executive.jpg", "Attendance packs over thin links — Matrix when the fleet is meshed."),
            ("Plant & Site Ops", "images/eyenet-industrial.jpg", "Industrial zones, contractors, and fall-prone floors under one stack."),
        ],
        "apps": [
            ("Presence", "Crew and site presence with automatic check-in across gates and posts.", "Access Control", "Area · Gate"),
            ("Matrix", "Fleet and multi-site aggregated reporting over VPN with degraded mode.", "Enterprise", "All Modes"),
        ],
        "modes": ["Gate Mode", "Area Mode", "Spot Mode"],
        "deep": {
            "app": "Matrix",
            "blurb": "Ships and industrial sites cannot lean on cloud VMS when links are thin. EyeNet keeps local truth about who is onboard or on site, packs reports for shore or HQ, and covers fall-critical zones so a fall becomes an immediate alert.",
            "features": [
                ("Industrial site zones", "Restricted areas, yards, and production floors."),
                ("Fall detection", "Decks, holds, warehouses, and industrial floors."),
                ("Shift & contractor presence", "Who is on site without badge chasing."),
                ("Exact onboard count", "Precise headcount at any moment."),
                ("Shore & HQ reports", "Automated attendance packs to fleet HQ or plant control."),
                ("Fleet / site Matrix", "VPN mesh; degraded mode — no data loss offline."),
            ],
            "users": "Maritime operators, fleet managers, shore HQ, plant / site ops, and industrial security.",
            "modes": "Gate, Area, Spot — aggregated via Matrix",
        },
    },
]

MODE_COPY = {
    "Spot Mode": "Precise monitoring of fixed, close-range areas",
    "Gate Mode": "Comprehensive monitoring of entrances, exits, corridors",
    "Area Mode": "Wide-area surveillance for large spaces",
    "Goggles Mode": "Mobile, first-person monitoring via wearable tech",
    "Drone Mode": "Aerial surveillance, mobile perspective coverage",
}

MODE_ICONS = {
    "Spot Mode": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "Gate Mode": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/>',
    "Area Mode": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "Goggles Mode": '<path d="M2 7h5.5L12 2l4.5 5H22v10H2z"/><circle cx="9" cy="12" r="2"/><circle cx="15" cy="12" r="2"/>',
    "Drone Mode": '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="18" r="3"/><rect x="9" y="9" width="6" height="6" rx="1"/>',
}


def asset(path: str, depth: int = 1) -> str:
    prefix = "../" * depth
    if path.startswith("images/") or path.startswith("cases/") or path.startswith("screenshots/"):
        return f"{prefix}assets/images/{path}" if not path.startswith("images/") else f"{prefix}assets/{path}"
    return f"{prefix}assets/images/{path}"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nav_html(active: str | None, depth: int = 1) -> str:
    prefix = "../" * depth if depth else ""
    links = [f'<a href="{prefix}index.html">Hub</a>']
    for c in CASES:
        cls = ' class="is-active"' if c["slug"] == active else ""
        href = f'{prefix}{c["slug"]}/' if depth else f'{c["slug"]}/'
        if depth == 0:
            href = f'{c["slug"]}/'
        links.append(f'<a href="{href}"{cls}>{esc(c["nav"])}</a>')
    links.append('<span class="nav-sep" aria-hidden="true"></span>')
    links.append('<a href="https://eyenet-vision.com/" rel="noopener">Product</a>')
    return '<nav class="micro-nav" aria-label="Marketing sites">' + "".join(links) + "</nav>"


def fab_html(*, product: bool = True, hub_href: str = "../index.html") -> str:
    """Sticky floating CTAs between product site and use-case hub."""
    bits = ['<aside class="site-fab" aria-label="Quick links">']
    if product:
        bits.append(
            '<a class="site-fab-primary" href="https://eyenet-vision.com/" rel="noopener">Product site</a>'
        )
        bits.append(
            '<a href="https://eyenet-vision.com/#primary-use-cases" rel="noopener">Case index</a>'
        )
    bits.append(f'<a href="{hub_href}">All use cases</a>')
    bits.append("</aside>")
    return "\n    ".join(bits)


def card_html(card: dict, depth: int = 1) -> str:
    cid = f' id="{card["id"]}"' if card.get("id") else ""
    stats = "".join(
        f'<div class="stat-item"><span class="stat-value{" cyan" if i == 0 else ""}">{esc(v)}</span><span class="stat-label">{esc(l)}</span></div>'
        for i, (v, l) in enumerate(card["stats"])
    )
    feats = "".join(
        f'<div class="feature-item"><div class="feature-head"><span class="accent-dot"></span>{esc(h)}</div><p class="feature-desc">{esc(d)}</p></div>'
        for h, d in card["features"]
    )
    chip_id = f'chips-{card.get("id") or card["label"].lower().replace(" ", "-")}'
    return f'''
    <section{cid}>
        <div class="content-panel">
            <div class="section-label">{esc(card["label"])}</div>
            <h2 class="card-headline small">{card["headline"]}</h2>
            <div class="image-strip" style="margin-bottom: 4rem;">
                <img src="{asset(card["image"], depth)}" alt="{esc(card["label"])}" loading="lazy">
            </div>
            <div class="hairline-cyan" style="margin-bottom: 2rem;"></div>
            <div class="stat-collection" style="margin-bottom: 2rem;">{stats}</div>
            <div class="hairline" style="margin-bottom: 2rem;"></div>
            <div class="feature-grid" style="margin-bottom: 2rem;">{feats}</div>
            <div class="chip-row" id="{chip_id}" data-chips="{esc(card["chips"])}"></div>
            <div class="cta-pair">
                <a href="{card["cta_href"]}" class="cta-link">{esc(card["cta"])} <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
                <a href="https://eyenet-vision.com/" class="cta-link cta-link-case" rel="noopener">Product platform <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
            </div>
        </div>
    </section>
    <div class="hairline"></div>
'''


def render_case(case: dict) -> str:
    depth = 1
    w = case["wedge"]
    wedge_stats = "".join(
        f'<div class="stat-item"><span class="stat-value{" cyan" if i != 1 else ""}">{esc(v)}</span><span class="stat-label">{esc(l)}</span></div>'
        for i, (v, l) in enumerate(w["stats"])
    )
    wedge_feats = "".join(
        f'<div class="feature-item"><div class="feature-head"><span class="accent-dot"></span>{esc(h)}</div><p class="feature-desc">{esc(d)}</p></div>'
        for h, d in w["features"]
    )
    cards = "".join(card_html(c, depth) for c in case["cards"])
    shots = "".join(
        f'''<div class="gallery-item" onclick="openLightbox('{asset(src, depth)}','{esc(title)}','{esc(desc)}')">
            <img src="{asset(src, depth)}" alt="{esc(title)}" loading="lazy">
            <div class="gallery-caption"><p>{esc(title)}</p></div>
        </div>'''
        for src, title, desc in case["screenshots"]
    )
    roles = "".join(
        f'''<div class="role-card" style="background:#000">
            <div class="feature-head" style="margin-bottom:1rem"><span class="accent-dot"></span>{esc(name)}</div>
            <img src="{asset(img, depth)}" alt="{esc(name)}" loading="lazy">
            <p style="font-size:0.85rem;color:rgba(255,255,255,0.45);line-height:1.5">{esc(blurb)}</p>
        </div>'''
        for name, img, blurb in case["roles"]
    )
    apps = "".join(
        f'''<div class="app-suite-card">
            <div class="app-suite-headline" data-app-name="{esc(name)}"></div>
            <p style="margin-bottom:1rem">{esc(blurb)}</p>
            <div><span class="minimal-badge">{esc(badge)}</span></div>
            <div style="margin-top:0.75rem;font-size:0.85rem;color:rgba(255,255,255,0.35)"><span style="font-weight:600">Modes:</span> {esc(modes)}</div>
        </div>'''
        for name, blurb, badge, modes in case["apps"]
    )
    modes = "".join(
        f'''<div class="flowchart-node" style="background:#000">
            <svg class="app-icon" style="margin:0 auto 0.75rem;display:block" viewBox="0 0 24 24">{MODE_ICONS[m]}</svg>
            <p style="font-weight:600;color:#fff">{esc(m)}</p>
            <p style="font-size:0.8rem;color:rgba(255,255,255,0.4)">{esc(MODE_COPY[m])}</p>
        </div>'''
        for m in case["modes"]
    )
    deep = case["deep"]
    deep_feats = "".join(f"<li><strong>{esc(k)}</strong> — {esc(v)}</li>" for k, v in deep["features"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(case["title"])} — Eyenet</title>
    <meta name="description" content="{esc(case["tease"])}">
    <link rel="icon" href="../assets/eyenet-dark.svg" type="image/svg+xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../assets/site.css">
</head>
<body>
    {nav_html(case["slug"], depth)}
    {fab_html(product=True, hub_href="../index.html")}

    <header class="header-hero">
        <div class="header-bg">
            <img src="{asset(case["hero_img"], depth)}" alt="">
        </div>
        <div class="header-veil"></div>
        <div class="header-cyan-wash"></div>
        <div class="header-content">
            <h1 class="header-headline">{case["hero_html"]}</h1>
            <div class="header-accent-line"></div>
            {LOGO_SVG}
            <p style="margin-top:1.5rem;font-size:0.95rem;font-weight:300;color:rgba(255,255,255,0.5);max-width:560px;margin-left:auto;margin-right:auto;line-height:1.5">{esc(case["who"])}</p>
        </div>
    </header>

    <div class="hairline"></div>

    <section>
        <div class="content-panel">
            <div class="section-label">{esc(w["label"])}</div>
            <h2 class="card-headline">{w["headline"]}</h2>
            <div class="image-strip" style="margin-bottom: 4rem;">
                <img src="{asset(w["image"], depth)}" alt="{esc(w["label"])}" loading="lazy">
            </div>
            <div class="hairline-cyan" style="margin-bottom: 2rem;"></div>
            <div class="stat-collection">{wedge_stats}</div>
            <div class="hairline" style="margin-bottom: 2rem;"></div>
            <div class="feature-grid">{wedge_feats}</div>
            <div class="chip-row" id="chips-wedge" data-chips="{esc(w["chips"])}"></div>
            <div class="cta-pair">
                <a href="#cap-0" class="cta-link">See how it works <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
                <a href="https://eyenet-vision.com/" class="cta-link cta-link-case" rel="noopener">Product platform <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
            </div>
        </div>
    </section>
    <div class="hairline"></div>

    <div id="cap-0"></div>
    {cards}

    <section><div class="quote-block"><p>{esc(case["quote"])}</p><div class="heading-accent-line" style="margin-bottom: 0;"></div></div></section>
    <div class="hairline"></div>

    <section id="in-action">
        <div class="content-panel wide">
            <h2 class="section-heading"><em>Eyenet</em> in Action</h2>
            <p class="section-subheading">{esc(case["tease"])}</p>
            <div class="photo-strip-wrapper">
                <div class="photo-fade-l"></div>
                <div class="photo-fade-r"></div>
                <div class="photo-strip">{shots}</div>
            </div>
        </div>
    </section>
    <div class="hairline"></div>

    <section>
        <div class="content-panel wide">
            <h2 class="section-heading">Value Across <em>Every Role</em></h2>
            <p class="section-subheading">Stakeholders who win when this wedge is live</p>
            <div class="roles-grid">{roles}</div>
        </div>
    </section>
    <div class="hairline"></div>

    <section>
        <div class="content-panel wide">
            <h2 class="section-heading">Application <em>Focus</em></h2>
            <p class="section-subheading">The EyeNet applications that power this use case</p>
            <div class="app-suite-grid">{apps}</div>
        </div>
    </section>
    <div class="hairline"></div>

    <section id="operating-modes">
        <div class="content-panel">
            <h2 class="section-heading">Operating <em>Modes</em></h2>
            <p class="section-subheading">Deployment configurations for this wedge</p>
            <div style="display:flex;flex-direction:column;align-items:center">
                <div class="flowchart-node" style="margin-bottom:1.5rem;width:100%;max-width:320px">
                    <svg class="app-icon" style="margin:0 auto 0.75rem;display:block" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                    <p style="font-weight:600;color:#fff">Camera Input</p>
                    <p style="font-size:0.85rem;color:rgba(255,255,255,0.4)">Central data acquisition for visual intelligence</p>
                </div>
                <div class="flowchart-connector" style="height:2rem"></div>
                <div class="modes-grid">{modes}</div>
            </div>
        </div>
    </section>
    <div class="hairline"></div>

    <section>
        <div class="content-panel wide">
            <h2 class="section-heading">Application <em>Deep Dive</em></h2>
            <p class="section-subheading">Capabilities and target users for this wedge</p>
            <div class="deep-dive-card" style="background:#000">
                <div class="deep-dive-headline" data-dd-name="{esc(deep["app"])}"></div>
                <p style="color:rgba(255,255,255,0.45);margin:1rem 0 1.5rem;line-height:1.5;text-align:left">{esc(deep["blurb"])}</p>
                <p style="font-weight:600;color:rgba(255,255,255,0.65);margin-bottom:0.5rem;text-align:left">Key Features:</p>
                <ul class="deep-list">{deep_feats}</ul>
                <p style="font-weight:600;color:rgba(255,255,255,0.65);margin:1.5rem 0 0.5rem;text-align:left">Target Users:</p>
                <p class="target-users" style="text-align:left;margin:0">{esc(deep["users"])}</p>
                <p style="font-weight:600;color:rgba(255,255,255,0.65);margin:1.5rem 0 0.5rem;text-align:left">Available Modes:</p>
                <p class="target-users" style="text-align:left;margin:0">{esc(deep["modes"])}</p>
            </div>
        </div>
    </section>
    <div class="hairline"></div>

    <section class="close-cta-panel">
        <div class="section-label">Next</div>
        <h2 class="section-heading">Ready to <em>deploy</em> this wedge?</h2>
        <p class="section-subheading" style="margin-bottom:0">Jump to the product site, the cite-backed value page, or the full use-case hub.</p>
        <div class="cta-row">
            <a class="cta-link" href="https://eyenet-vision.com/" rel="noopener">Product site</a>
            <a class="cta-link" href="https://eyenet-vision.com/#primary-use-cases" rel="noopener">Case index on product</a>
            <a class="cta-link" href="https://value.eyenet-vision.com/why/{case["slug"]}/" rel="noopener">Value analysis</a>
            <a class="cta-link" href="../index.html">All use cases</a>
        </div>
    </section>

    <section style="padding:6rem 2rem;text-align:center">{FOOTER_LOGO}</section>
    <footer style="padding:4rem;text-align:center">
        <p style="font-size:0.8rem;font-weight:300;color:rgba(255,255,255,0.35);letter-spacing:0.1em;text-transform:uppercase">&copy; 2026 Eyenet. All rights reserved.</p>
    </footer>

    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)"><div class="lightbox-content" onclick="event.stopPropagation()"><button class="lightbox-close" onclick="closeLightbox()">&times;</button><img id="lightbox-image" class="lightbox-image" src="" alt=""><div style="padding:1rem;background:#111;color:rgba(255,255,255,0.7)"><h3 id="lightbox-title" style="color:#22d3ee;font-size:1.25rem;font-weight:700;margin-bottom:0.5rem"></h3><p id="lightbox-description"></p></div></div></div>
    <script src="../assets/site.js"></script>
</body>
</html>
'''


def render_hub() -> str:
    entries = []
    for i, c in enumerate(CASES, 1):
        entries.append(f'''
        <a class="hub-entry" href="{c["slug"]}/">
            <div class="hub-entry-bg"><img src="{asset(c["hero_img"], 0)}" alt=""></div>
            <div class="hub-entry-veil"></div>
            <div class="hub-entry-body">
                <div class="hub-entry-num">Case {i:02d}</div>
                <h2 class="hub-entry-title">{c["hero_html"]}</h2>
                <p class="hub-entry-tease">{esc(c["tease"])}</p>
                <div class="hub-entry-cta">Enter microsite →</div>
            </div>
        </a>''')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eyenet Marketing — Use-Case Microsites</title>
    <meta name="description" content="Daring EyeNet marketing microsites for every primary use case.">
    <link rel="icon" href="assets/eyenet-dark.svg" type="image/svg+xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/site.css">
</head>
<body>
    {nav_html(None, 0)}

    <header class="header-hero" style="height:78vh;min-height:520px">
        <div class="header-bg">
            <img src="assets/images/hero-eye.png" alt="">
        </div>
        <div class="header-veil"></div>
        <div class="header-cyan-wash"></div>
        <div class="header-content">
            <h1 class="header-headline">EyeNet for the <em>moments that matter</em></h1>
            <div class="header-accent-line"></div>
            {LOGO_SVG}
            <p style="margin-top:1.75rem;font-size:1.05rem;font-weight:300;color:rgba(255,255,255,0.55);max-width:560px;margin-left:auto;margin-right:auto;line-height:1.5">Seven primary use cases. Same machine vision platform. Enter the wedge that matches your world.</p>
        </div>
    </header>

    <div class="hairline"></div>

    <section>
        <div class="content-panel" style="padding-bottom:3rem">
            <div class="section-label">Use Cases</div>
            <h2 class="section-heading">Choose your <em>wedge</em></h2>
            <p class="section-subheading">Each microsite mirrors the product site structure — remapped to one daring operational story.</p>
        </div>
        <div class="hub-entries">{''.join(entries)}</div>
    </section>

    <div class="hairline"></div>

    <section class="close-cta-panel">
        <div class="section-label">Platform</div>
        <h2 class="section-heading">See the full <em>product</em></h2>
        <p class="section-subheading" style="margin-bottom:0">The complete EyeNet platform narrative, or the cite-backed value wiki behind these wedges.</p>
        <div class="cta-row">
            <a class="cta-link" href="https://eyenet-vision.com/" rel="noopener">Product site</a>
            <a class="cta-link" href="https://eyenet-vision.com/#primary-use-cases" rel="noopener">Case index on product</a>
            <a class="cta-link" href="https://value.eyenet-vision.com/why/" rel="noopener">Value cases</a>
        </div>
    </section>

    <section style="padding:6rem 2rem;text-align:center">{FOOTER_LOGO}</section>
    <footer style="padding:4rem;text-align:center">
        <p style="font-size:0.8rem;font-weight:300;color:rgba(255,255,255,0.35);letter-spacing:0.1em;text-transform:uppercase">&copy; 2026 Eyenet. All rights reserved.</p>
    </footer>
    <script src="assets/site.js"></script>
</body>
</html>
'''


def main() -> None:
    # Hub index.html is hand-maintained (chapter UX). Refresh case microsites only.
    for case in CASES:
        out = ROOT / case["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_case(case))
        print(f"Wrote {out}")
    print("Skipped hub index.html (hand-maintained)")


if __name__ == "__main__":
    main()
