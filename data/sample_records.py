
sample_records = [
    {
        "section": "177",
        "offence": "General provision for contravention of the Motor Vehicles Act, rules, regulations or notifications where no other penalty is provided.",
        "max_fine_first": 500,
        "max_fine_repeat": 1500,
        "other_action": "First offence: fine up to ₹500. Second or subsequent offence: fine up to ₹1,500.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "General Traffic Violation"
    },
    {
        "section": "179",
        "offence": "Wilfully disobeying lawful directions, obstructing an authorised person or authority, withholding required information, or knowingly providing false information.",
        "max_fine_first": 2000,
        "max_fine_repeat": None,
        "other_action": "Under subsection (2), imprisonment up to one month, or fine up to ₹2,000, or both. The section does not specify a separate repeat-offence fine.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Traffic Authority Compliance"
    },
    {
        "section": "180",
        "offence": "An owner or person in charge of a motor vehicle allowing a person who does not satisfy the requirements of section 3 or section 4 to drive.",
        "max_fine_first": 5000,
        "max_fine_repeat": None,
        "other_action": "Imprisonment up to three months, or fine up to ₹5,000, or both. No separate repeat-offence amount is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Licensing and Authorisation"
    },
    {
        "section": "181",
        "offence": "Driving a motor vehicle in contravention of section 3 (necessity for driving licence) or section 4 (age limit).",
        "max_fine_first": 5000,
        "max_fine_repeat": None,
        "other_action": "Imprisonment up to three months, or fine up to ₹5,000, or both. No separate repeat-offence amount is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Licensing and Authorisation"
    },
    {
        "section": "182",
        "offence": "Driving while disqualified from holding or obtaining a driving licence, or specified offences involving obtaining a driving or conductor's licence without disclosing required endorsements.",
        "max_fine_first": 10000,
        "max_fine_repeat": None,
        "other_action": "Subsection (1): imprisonment up to three months, or fine up to ₹10,000, or both; a driving licence obtained in the specified circumstances has no effect. Subsection (2): conductor's licence offences carry imprisonment up to one month, or fine up to ₹10,000, or both. No separate repeat-offence amount is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Licensing and Authorisation"
    },
    {
        "section": "183",
        "offence": "Driving, or causing or permitting a person under one's control to drive, in contravention of speed limits under section 112.",
        "max_fine_first": 4000,
        "max_fine_repeat": None,
        "other_action": "Light motor vehicle: fine ₹1,000–₹2,000. Medium or heavy goods/passenger vehicle: fine ₹2,000–₹4,000. For a second or subsequent offence under subsection (1), the driving licence is impounded under section 206(4).",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Driving Safety"
    },
    {
        "section": "184",
        "offence": "Driving at a speed or in a manner dangerous to the public, or causing alarm or distress to vehicle occupants, other road users or people near roads.",
        "max_fine_first": 5000,
        "max_fine_repeat": 10000,
        "other_action": "First offence: imprisonment from six months up to one year, or fine ₹1,000–₹5,000, or both. Second or subsequent similar offence within three years: imprisonment up to two years, or fine ₹10,000, or both. Includes specified dangerous acts such as jumping red lights, violating stop signs and handheld phone use while driving.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Dangerous Driving"
    },
    {
        "section": "185",
        "offence": "Driving or attempting to drive with alcohol exceeding 30 mg per 100 ml of blood, or under the influence of drugs to the extent of being incapable of exercising proper control over the vehicle.",
        "max_fine_first": 10000,
        "max_fine_repeat": 15000,
        "other_action": "First offence: imprisonment up to six months, or fine ₹10,000, or both. Second or subsequent offence: imprisonment up to two years, or fine ₹15,000, or both.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Driving Safety"
    },
    {
        "section": "186",
        "offence": "Driving in a public place while knowingly suffering from a disease or disability that may make driving dangerous to the public.",
        "max_fine_first": 1000,
        "max_fine_repeat": 2000,
        "other_action": "First offence: fine up to ₹1,000. Second or subsequent offence: fine up to ₹2,000.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Driving Safety"
    },
    {
        "section": "189",
        "offence": "Permitting or taking part in a race or trial of speed between motor vehicles in a public place without written consent of the State Government.",
        "max_fine_first": 5000,
        "max_fine_repeat": 10000,
        "other_action": "First offence: imprisonment up to three months, or fine up to ₹5,000, or both. Subsequent offence: imprisonment up to one year, or fine up to ₹10,000, or both.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Dangerous Driving"
    },
    {
        "section": "190",
        "offence": "Using or allowing the use of a vehicle in an unsafe condition, including dangerous defects, violations of prescribed road safety/noise/air-pollution standards, or improper carriage of dangerous or hazardous goods.",
        "max_fine_first": 10000,
        "max_fine_repeat": 20000,
        "other_action": "Subsection (1): ordinary dangerous defect fine up to ₹1,500; where an accident causes bodily injury or property damage, imprisonment up to three months or fine up to ₹5,000 or both. Subsequent accident-related offence: imprisonment up to six months or fine up to ₹10,000 or both. Subsection (2): first offence imprisonment up to three months or fine up to ₹10,000 or both, plus three-month licence disqualification; subsequent offence imprisonment up to six months or fine up to ₹10,000 or both. Subsection (3): dangerous/hazardous goods first offence fine ₹10,000 plus three-month licence disqualification; subsequent offence fine ₹20,000 or imprisonment up to three years or both.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Vehicle Safety and Compliance"
    },
    {
        "section": "192",
        "offence": "Driving, causing or allowing a motor vehicle to be used in contravention of the registration requirements under section 39.",
        "max_fine_first": 5000,
        "max_fine_repeat": 10000,
        "other_action": "First offence: fine ₹2,000–₹5,000. Second or subsequent offence: imprisonment up to one year, or fine ₹5,000–₹10,000, or both. The section contains an emergency-use exception subject to reporting to the Regional Transport Authority within seven days. A vehicle without a required fitness certificate is treated as unregistered under the stated provision.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Registration and Documentation"
    },
    {
        "section": "192A",
        "offence": "Driving, causing or allowing a motor vehicle to be used without the required permit under section 66(1), or contrary to specified permit conditions relating to route, area or purpose.",
        "max_fine_first": 10000,
        "max_fine_repeat": 10000,
        "other_action": "First offence: imprisonment up to six months, or fine ₹10,000, or both. Subsequent offence: imprisonment from six months up to one year, or fine ₹10,000, or both. Emergency-use exceptions apply subject to reporting to the Regional Transport Authority within seven days.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Permit and Authorisation"
    },
    {
        "section": "194",
        "offence": "Driving, causing or allowing a motor vehicle to be driven in contravention of permissible weight or load requirements under sections 113, 114 or 115.",
        "max_fine_first": None,
        "max_fine_repeat": None,
        "other_action": "Subsection (1): ₹20,000 plus ₹2,000 per tonne of excess load, together with off-loading charges. The vehicle cannot move until excess load is removed. Subsection (1A): improper load projection beyond permissible dimensions carries ₹20,000 plus off-loading charges. Subsection (2): refusing weighing or removing load before weighing carries a fine of ₹40,000. The section does not specify a separate repeat-offence fine for these provisions.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Vehicle Safety and Compliance"
    },
    {
        "section": "194A",
        "offence": "Driving, causing or allowing a transport vehicle to carry more passengers than authorised in its registration certificate or permit conditions.",
        "max_fine_first": None,
        "max_fine_repeat": None,
        "other_action": "Fine of ₹200 per excess passenger. The transport vehicle cannot move until excess passengers are off-loaded and alternative transport is arranged. The provision does not specify a separate repeat-offence amount or a fixed maximum total.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Passenger Safety"
    },
    {
        "section": "194B",
        "offence": "Driving without wearing a safety belt, carrying passengers not wearing seat belts, or carrying a child under 14 who is not secured by a safety belt or child restraint system.",
        "max_fine_first": 1000,
        "max_fine_repeat": None,
        "other_action": "Fine of ₹1,000 under subsection (1) and ₹1,000 under subsection (2). The State Government may exempt specified categories of transport vehicles from subsection (1) by Gazette notification. No separate repeat-offence amount is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Passenger Safety"
    },
    {
        "section": "194C",
        "offence": "Driving or allowing a motorcycle to be driven in violation of safety measures under section 128 or rules/regulations made under it, concerning motorcycle drivers and pillion riders.",
        "max_fine_first": 1000,
        "max_fine_repeat": None,
        "other_action": "Fine of ₹1,000 and disqualification from holding a driving licence for three months. No separate repeat-offence fine is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Passenger Safety"
    },
    {
        "section": "194D",
        "offence": "Driving or allowing a motorcycle to be driven in violation of protective headgear requirements under section 129 or rules/regulations made under it.",
        "max_fine_first": 1000,
        "max_fine_repeat": None,
        "other_action": "Fine of ₹1,000 and disqualification from holding a driving licence for three months. No separate repeat-offence fine is specified.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Passenger Safety"
    },
    {
        "section": "194E",
        "offence": "Failing to draw to the side of the road when a fire service vehicle, ambulance or other specified emergency vehicle approaches.",
        "max_fine_first": 10000,
        "max_fine_repeat": None,
        "other_action": "Imprisonment up to six months, or fine up to ₹10,000, or both. The supplied PDF does not specify a separate repeat-offence penalty.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Emergency Vehicle Compliance"
    },
    {
        "section": "196",
        "offence": "Driving, causing or allowing a motor vehicle to be driven without the insurance required under section 146.",
        "max_fine_first": 2000,
        "max_fine_repeat": 4000,
        "other_action": "First offence: imprisonment up to three months, or fine up to ₹2,000, or both. Subsequent offence: imprisonment up to three months, or fine up to ₹4,000, or both.",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/1798/1/a1988-59.pdf",
        "category": "Insurance and Documentation"
    }
]
