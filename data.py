"""
50 dummy human records with fraud risk scores.
- phone_risk, email_risk, address_risk, ip_risk: 0.0–1.0 (2 decimal places)
- overall_risk: 1–500
"""

PEOPLE = [
    {
        "id": 1, "name": "Alice Harmon", "phone": "+1-212-555-0101",
        "email": "alice.harmon@gmail.com", "ip": "72.14.204.99",
        "address": "14 Oak Street, Brooklyn, NY 11201",
        "phone_risk": 0.05, "email_risk": 0.03, "address_risk": 0.07, "ip_risk": 0.04,
        "overall_risk": 12,
    },
    {
        "id": 2, "name": "Carlos Mendez", "phone": "+1-415-555-0202",
        "email": "c.mendez99@yahoo.com", "ip": "185.220.101.45",
        "address": "300 Mission St, San Francisco, CA 94105",
        "phone_risk": 0.72, "email_risk": 0.68, "address_risk": 0.55, "ip_risk": 0.91,
        "overall_risk": 418,
    },
    {
        "id": 3, "name": "Priya Sharma", "phone": "+1-312-555-0303",
        "email": "priya.sharma@outlook.com", "ip": "104.16.132.229",
        "address": "221 W Wacker Dr, Chicago, IL 60606",
        "phone_risk": 0.12, "email_risk": 0.08, "address_risk": 0.10, "ip_risk": 0.11,
        "overall_risk": 28,
    },
    {
        "id": 4, "name": "Derek Fowler", "phone": "+1-713-555-0404",
        "email": "derek.f@tempmail.com", "ip": "5.188.86.172",
        "address": "1001 Main St, Houston, TX 77002",
        "phone_risk": 0.81, "email_risk": 0.95, "address_risk": 0.44, "ip_risk": 0.87,
        "overall_risk": 462,
    },
    {
        "id": 5, "name": "Sofia Ricci", "phone": "+1-305-555-0505",
        "email": "sofricci@icloud.com", "ip": "173.194.79.103",
        "address": "800 Brickell Ave, Miami, FL 33131",
        "phone_risk": 0.09, "email_risk": 0.06, "address_risk": 0.08, "ip_risk": 0.05,
        "overall_risk": 17,
    },
    {
        "id": 6, "name": "James Okafor", "phone": "+1-404-555-0606",
        "email": "james.okafor@protonmail.com", "ip": "45.148.10.22",
        "address": "275 Peachtree St NE, Atlanta, GA 30303",
        "phone_risk": 0.43, "email_risk": 0.37, "address_risk": 0.29, "ip_risk": 0.61,
        "overall_risk": 187,
    },
    {
        "id": 7, "name": "Mei-Ling Chen", "phone": "+1-206-555-0707",
        "email": "meiling.chen@gmail.com", "ip": "66.249.64.220",
        "address": "600 Pine St, Seattle, WA 98101",
        "phone_risk": 0.07, "email_risk": 0.04, "address_risk": 0.06, "ip_risk": 0.09,
        "overall_risk": 19,
    },
    {
        "id": 8, "name": "Brandon Walsh", "phone": "+1-702-555-0808",
        "email": "bwalsh_1337@mailinator.com", "ip": "91.108.4.56",
        "address": "3600 S Las Vegas Blvd, Las Vegas, NV 89109",
        "phone_risk": 0.67, "email_risk": 0.88, "address_risk": 0.73, "ip_risk": 0.79,
        "overall_risk": 389,
    },
    {
        "id": 9, "name": "Amara Diallo", "phone": "+1-617-555-0909",
        "email": "amara.diallo@harvard.edu", "ip": "128.103.1.1",
        "address": "124 Mt Auburn St, Cambridge, MA 02138",
        "phone_risk": 0.04, "email_risk": 0.02, "address_risk": 0.05, "ip_risk": 0.03,
        "overall_risk": 8,
    },
    {
        "id": 10, "name": "Tyler Brooks", "phone": "+1-503-555-1010",
        "email": "tyler_b@disposablemail.net", "ip": "185.56.83.144",
        "address": "1000 SW Broadway, Portland, OR 97205",
        "phone_risk": 0.59, "email_risk": 0.91, "address_risk": 0.38, "ip_risk": 0.84,
        "overall_risk": 356,
    },
    {
        "id": 11, "name": "Natasha Volkov", "phone": "+1-202-555-1111",
        "email": "n.volkov@state.gov", "ip": "192.168.10.5",
        "address": "2201 C St NW, Washington, DC 20520",
        "phone_risk": 0.11, "email_risk": 0.07, "address_risk": 0.09, "ip_risk": 0.12,
        "overall_risk": 24,
    },
    {
        "id": 12, "name": "Omar Hassan", "phone": "+1-612-555-1212",
        "email": "omar.h77@webmail.com", "ip": "185.234.218.101",
        "address": "50 S 6th St, Minneapolis, MN 55402",
        "phone_risk": 0.56, "email_risk": 0.63, "address_risk": 0.49, "ip_risk": 0.77,
        "overall_risk": 301,
    },
    {
        "id": 13, "name": "Laura Kim", "phone": "+1-619-555-1313",
        "email": "laurakim@gmail.com", "ip": "74.125.68.100",
        "address": "101 W Broadway, San Diego, CA 92101",
        "phone_risk": 0.08, "email_risk": 0.05, "address_risk": 0.07, "ip_risk": 0.06,
        "overall_risk": 15,
    },
    {
        "id": 14, "name": "Marcus Bell", "phone": "+1-313-555-1414",
        "email": "m.bell2024@fakeinbox.com", "ip": "194.165.16.78",
        "address": "400 Renaissance Dr, Detroit, MI 48243",
        "phone_risk": 0.74, "email_risk": 0.86, "address_risk": 0.61, "ip_risk": 0.82,
        "overall_risk": 432,
    },
    {
        "id": 15, "name": "Ingrid Larsson", "phone": "+1-612-555-1515",
        "email": "ingrid.larsson@icloud.com", "ip": "17.253.144.10",
        "address": "222 S 9th St, Minneapolis, MN 55402",
        "phone_risk": 0.10, "email_risk": 0.09, "address_risk": 0.11, "ip_risk": 0.08,
        "overall_risk": 22,
    },
    {
        "id": 16, "name": "Raphael Torres", "phone": "+1-480-555-1616",
        "email": "rtorres@anonymousmail.io", "ip": "45.33.32.156",
        "address": "7500 E McCormick Pkwy, Scottsdale, AZ 85258",
        "phone_risk": 0.51, "email_risk": 0.79, "address_risk": 0.34, "ip_risk": 0.68,
        "overall_risk": 278,
    },
    {
        "id": 17, "name": "Hannah Scott", "phone": "+1-901-555-1717",
        "email": "hscott@memphisuniv.edu", "ip": "141.225.1.1",
        "address": "3720 Alumni Ave, Memphis, TN 38152",
        "phone_risk": 0.06, "email_risk": 0.03, "address_risk": 0.05, "ip_risk": 0.04,
        "overall_risk": 11,
    },
    {
        "id": 18, "name": "Liang Wu", "phone": "+1-626-555-1818",
        "email": "liang.wu99@mail.com", "ip": "112.29.33.210",
        "address": "168 E Colorado Blvd, Pasadena, CA 91105",
        "phone_risk": 0.38, "email_risk": 0.44, "address_risk": 0.31, "ip_risk": 0.55,
        "overall_risk": 168,
    },
    {
        "id": 19, "name": "Elena Papadopoulos", "phone": "+1-773-555-1919",
        "email": "elena.p@mailnull.com", "ip": "185.100.87.202",
        "address": "55 E Monroe St, Chicago, IL 60603",
        "phone_risk": 0.63, "email_risk": 0.75, "address_risk": 0.58, "ip_risk": 0.89,
        "overall_risk": 368,
    },
    {
        "id": 20, "name": "David Nguyen", "phone": "+1-408-555-2020",
        "email": "dnguyen@apple.com", "ip": "17.178.96.7",
        "address": "1 Apple Park Way, Cupertino, CA 95014",
        "phone_risk": 0.03, "email_risk": 0.02, "address_risk": 0.04, "ip_risk": 0.03,
        "overall_risk": 6,
    },
    {
        "id": 21, "name": "Fatima Al-Sayed", "phone": "+1-214-555-2121",
        "email": "fatimaas@hotmail.com", "ip": "40.77.167.85",
        "address": "500 N Akard St, Dallas, TX 75201",
        "phone_risk": 0.14, "email_risk": 0.11, "address_risk": 0.13, "ip_risk": 0.10,
        "overall_risk": 31,
    },
    {
        "id": 22, "name": "Kevin Park", "phone": "+1-213-555-2222",
        "email": "k.park_anon@guerrillamail.com", "ip": "185.220.102.8",
        "address": "350 S Grand Ave, Los Angeles, CA 90071",
        "phone_risk": 0.69, "email_risk": 0.93, "address_risk": 0.47, "ip_risk": 0.96,
        "overall_risk": 447,
    },
    {
        "id": 23, "name": "Svetlana Ivanova", "phone": "+1-646-555-2323",
        "email": "s.ivanova@gmail.com", "ip": "209.85.231.104",
        "address": "1251 Avenue of the Americas, New York, NY 10020",
        "phone_risk": 0.17, "email_risk": 0.13, "address_risk": 0.15, "ip_risk": 0.12,
        "overall_risk": 38,
    },
    {
        "id": 24, "name": "Emmanuel Obi", "phone": "+1-832-555-2424",
        "email": "eobi_test@throwam.com", "ip": "37.19.200.52",
        "address": "811 Dallas St, Houston, TX 77002",
        "phone_risk": 0.58, "email_risk": 0.84, "address_risk": 0.42, "ip_risk": 0.71,
        "overall_risk": 321,
    },
    {
        "id": 25, "name": "Claire Dubois", "phone": "+1-504-555-2525",
        "email": "claire.dubois@louisiana.edu", "ip": "130.39.1.1",
        "address": "6363 St Charles Ave, New Orleans, LA 70118",
        "phone_risk": 0.05, "email_risk": 0.04, "address_risk": 0.06, "ip_risk": 0.05,
        "overall_risk": 13,
    },
    {
        "id": 26, "name": "Alexei Romanov", "phone": "+1-718-555-2626",
        "email": "alexei.r@protonmail.ch", "ip": "62.102.148.68",
        "address": "150 Court St, Brooklyn, NY 11201",
        "phone_risk": 0.46, "email_risk": 0.52, "address_risk": 0.33, "ip_risk": 0.64,
        "overall_risk": 213,
    },
    {
        "id": 27, "name": "Grace Thompson", "phone": "+1-303-555-2727",
        "email": "grace.t@comcast.net", "ip": "73.245.98.153",
        "address": "1670 Broadway, Denver, CO 80202",
        "phone_risk": 0.09, "email_risk": 0.07, "address_risk": 0.08, "ip_risk": 0.06,
        "overall_risk": 18,
    },
    {
        "id": 28, "name": "Antonio Ferrara", "phone": "+1-702-555-2828",
        "email": "aferrara99@yandex.com", "ip": "213.87.122.44",
        "address": "9999 Las Vegas Blvd S, Las Vegas, NV 89183",
        "phone_risk": 0.61, "email_risk": 0.57, "address_risk": 0.66, "ip_risk": 0.73,
        "overall_risk": 335,
    },
    {
        "id": 29, "name": "Yuki Tanaka", "phone": "+1-310-555-2929",
        "email": "yuki.tanaka@gmail.com", "ip": "216.58.217.68",
        "address": "11444 W Olympic Blvd, Los Angeles, CA 90064",
        "phone_risk": 0.06, "email_risk": 0.05, "address_risk": 0.07, "ip_risk": 0.04,
        "overall_risk": 14,
    },
    {
        "id": 30, "name": "Victor Adeyemi", "phone": "+1-312-555-3030",
        "email": "v.adeyemi_anon@fakeemail.net", "ip": "192.99.200.210",
        "address": "233 S Wacker Dr, Chicago, IL 60606",
        "phone_risk": 0.77, "email_risk": 0.89, "address_risk": 0.53, "ip_risk": 0.83,
        "overall_risk": 441,
    },
    {
        "id": 31, "name": "Rachel Evans", "phone": "+1-215-555-3131",
        "email": "rachel.evans@penn.edu", "ip": "128.91.1.1",
        "address": "3451 Walnut St, Philadelphia, PA 19104",
        "phone_risk": 0.04, "email_risk": 0.03, "address_risk": 0.05, "ip_risk": 0.04,
        "overall_risk": 9,
    },
    {
        "id": 32, "name": "Mohammed Al-Farsi", "phone": "+1-212-555-3232",
        "email": "malfarsi@mailinator.com", "ip": "185.117.88.16",
        "address": "9 W 57th St, New York, NY 10019",
        "phone_risk": 0.65, "email_risk": 0.81, "address_risk": 0.48, "ip_risk": 0.78,
        "overall_risk": 374,
    },
    {
        "id": 33, "name": "Sarah Johnson", "phone": "+1-901-555-3333",
        "email": "sjohnson@fedex.com", "ip": "199.193.128.100",
        "address": "942 S Shady Grove Rd, Memphis, TN 38120",
        "phone_risk": 0.07, "email_risk": 0.06, "address_risk": 0.08, "ip_risk": 0.07,
        "overall_risk": 16,
    },
    {
        "id": 34, "name": "Pedro Castillo", "phone": "+1-626-555-3434",
        "email": "pcastillo_fake@mailnesia.com", "ip": "91.92.109.44",
        "address": "160 W Colorado Blvd, Pasadena, CA 91105",
        "phone_risk": 0.54, "email_risk": 0.78, "address_risk": 0.39, "ip_risk": 0.69,
        "overall_risk": 298,
    },
    {
        "id": 35, "name": "Nina Kowalski", "phone": "+1-414-555-3535",
        "email": "nina.kowalski@gmail.com", "ip": "173.194.46.81",
        "address": "310 W Wisconsin Ave, Milwaukee, WI 53203",
        "phone_risk": 0.11, "email_risk": 0.09, "address_risk": 0.10, "ip_risk": 0.08,
        "overall_risk": 23,
    },
    {
        "id": 36, "name": "Jerome Lafleur", "phone": "+1-514-555-3636",
        "email": "j.lafleur@throwaway.email", "ip": "185.220.101.22",
        "address": "1250 René-Lévesque Blvd W, Montreal, QC H3B 4W8",
        "phone_risk": 0.48, "email_risk": 0.87, "address_risk": 0.35, "ip_risk": 0.90,
        "overall_risk": 387,
    },
    {
        "id": 37, "name": "Aisha Mohammed", "phone": "+1-602-555-3737",
        "email": "aisha.m@outlook.com", "ip": "40.112.72.205",
        "address": "2 N Central Ave, Phoenix, AZ 85004",
        "phone_risk": 0.13, "email_risk": 0.10, "address_risk": 0.12, "ip_risk": 0.09,
        "overall_risk": 27,
    },
    {
        "id": 38, "name": "Ryan O'Brien", "phone": "+1-617-555-3838",
        "email": "ryan.obrien@anon.im", "ip": "23.82.140.102",
        "address": "100 Federal St, Boston, MA 02110",
        "phone_risk": 0.52, "email_risk": 0.60, "address_risk": 0.41, "ip_risk": 0.66,
        "overall_risk": 243,
    },
    {
        "id": 39, "name": "Wendy Huang", "phone": "+1-206-555-3939",
        "email": "wendy.huang@amazon.com", "ip": "205.251.242.103",
        "address": "440 Terry Ave N, Seattle, WA 98109",
        "phone_risk": 0.04, "email_risk": 0.03, "address_risk": 0.05, "ip_risk": 0.04,
        "overall_risk": 7,
    },
    {
        "id": 40, "name": "Dimitri Papadakis", "phone": "+1-305-555-4040",
        "email": "d.papadakis@guerrillamail.net", "ip": "185.130.5.198",
        "address": "1221 Brickell Ave, Miami, FL 33131",
        "phone_risk": 0.70, "email_risk": 0.85, "address_risk": 0.62, "ip_risk": 0.94,
        "overall_risk": 453,
    },
    {
        "id": 41, "name": "Linda Patterson", "phone": "+1-919-555-4141",
        "email": "lpatterson@duke.edu", "ip": "152.3.1.1",
        "address": "305 Trent Dr, Durham, NC 27710",
        "phone_risk": 0.05, "email_risk": 0.04, "address_risk": 0.06, "ip_risk": 0.05,
        "overall_risk": 11,
    },
    {
        "id": 42, "name": "Hassan Karimi", "phone": "+1-469-555-4242",
        "email": "h.karimi_vpn@protonmail.com", "ip": "185.159.157.90",
        "address": "2200 Ross Ave, Dallas, TX 75201",
        "phone_risk": 0.62, "email_risk": 0.55, "address_risk": 0.45, "ip_risk": 0.88,
        "overall_risk": 326,
    },
    {
        "id": 43, "name": "Caitlin Murphy", "phone": "+1-503-555-4343",
        "email": "caitlin.murphy@gmail.com", "ip": "66.249.72.209",
        "address": "920 SW 6th Ave, Portland, OR 97204",
        "phone_risk": 0.08, "email_risk": 0.07, "address_risk": 0.09, "ip_risk": 0.06,
        "overall_risk": 18,
    },
    {
        "id": 44, "name": "Kwame Asante", "phone": "+1-404-555-4444",
        "email": "kasante_anon@mailinator.com", "ip": "91.108.56.108",
        "address": "101 Marietta St NW, Atlanta, GA 30303",
        "phone_risk": 0.76, "email_risk": 0.92, "address_risk": 0.57, "ip_risk": 0.85,
        "overall_risk": 446,
    },
    {
        "id": 45, "name": "Isabelle Martin", "phone": "+1-604-555-4545",
        "email": "isabelle.martin@canada.ca", "ip": "205.193.200.85",
        "address": "300 Georgia St W, Vancouver, BC V6B 6B4",
        "phone_risk": 0.06, "email_risk": 0.04, "address_risk": 0.07, "ip_risk": 0.05,
        "overall_risk": 14,
    },
    {
        "id": 46, "name": "Fernando Reyes", "phone": "+1-915-555-4646",
        "email": "freyes_unknown@10minutemail.com", "ip": "94.102.49.193",
        "address": "300 E Main Dr, El Paso, TX 79901",
        "phone_risk": 0.57, "email_risk": 0.90, "address_risk": 0.43, "ip_risk": 0.76,
        "overall_risk": 344,
    },
    {
        "id": 47, "name": "Olga Petrov", "phone": "+1-312-555-4747",
        "email": "olga.petrov@outlook.com", "ip": "65.52.128.33",
        "address": "200 E Randolph St, Chicago, IL 60601",
        "phone_risk": 0.16, "email_risk": 0.12, "address_risk": 0.14, "ip_risk": 0.11,
        "overall_risk": 35,
    },
    {
        "id": 48, "name": "Tyrone Jackson", "phone": "+1-901-555-4848",
        "email": "t.jackson_anon@guerrillamail.com", "ip": "185.220.100.240",
        "address": "5765 Shelby Oaks Dr, Memphis, TN 38134",
        "phone_risk": 0.83, "email_risk": 0.96, "address_risk": 0.71, "ip_risk": 0.98,
        "overall_risk": 489,
    },
    {
        "id": 49, "name": "Mei Zhang", "phone": "+1-408-555-4949",
        "email": "mei.zhang@visa.com", "ip": "8.34.208.152",
        "address": "900 Metro Center Blvd, Foster City, CA 94404",
        "phone_risk": 0.03, "email_risk": 0.02, "address_risk": 0.04, "ip_risk": 0.03,
        "overall_risk": 5,
    },
    {
        "id": 50, "name": "Nikolai Sorokin", "phone": "+1-718-555-5050",
        "email": "nsorokin_anon@protonmail.com", "ip": "185.220.101.66",
        "address": "30 Hudson Yards, New York, NY 10001",
        "phone_risk": 0.79, "email_risk": 0.73, "address_risk": 0.67, "ip_risk": 0.93,
        "overall_risk": 428,
    },
]


def get_risk_label(score: float) -> str:
    """Convert a 0-1 risk score to a human-readable label."""
    if score < 0.3:
        return "Low"
    elif score < 0.6:
        return "Medium"
    else:
        return "High"


def get_overall_risk_label(score: int) -> str:
    """Convert a 1-500 overall risk score to a human-readable label."""
    if score < 100:
        return "Low Risk"
    elif score < 250:
        return "Medium Risk"
    elif score < 400:
        return "High Risk"
    else:
        return "Critical Risk"
