# Day 7 — Semantic Search Evaluation

Search method: ChromaDB cosine similarity with section-aware reranking.

These are retrieved passages, not verified legal answers.
Lower distance means greater semantic similarity.
A missing distance indicates an exact-section candidate added during reranking.

## Question 1

**Question:** What is the fine for riding bike without helmet under section 194D?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 107
- Title: Motor Vehicles Act 1988
- Distance: 0.5004

**Retrieved passage:**

> o be driven with a child who, not having attained the age of fourteen years, is not secured by a safety belt or a child restraint system shall be 4[liable for a penalty] of one thousand rupees. 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders.— Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 128 or the rules or regulations made thereunder shall be 4[liable for a penalty] of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194D. Penalty for not wearing protective headgear.—Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 129 or the rules or regulations made

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 9
- Title: Motor Vehicles Act 1988
- Distance: 0.5352

**Retrieved passage:**

> 9 SECTIONS 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders. 194D. Penalty for not wearing protective headgear. 194E. Failure to allow free passage to emergency vehicles. 194F. Use of horns and silence zones. 195. [Omitted]. 196. Driving uninsured vehicle. 197. Taking vehicle without authority. 198. Unauthorised interference with vehicle. 198A. Failure to comply with standards for road design, construction and maintenance. 199. Offences by companies. 199A. Offences by juveniles. 199B. Revision of fines and penalties. 200. Composition of certain offences. 201. Penalty for causing obstruction to free flow of traffic. 202. Power to arrest without warrant. 203. Breath tests. 204. Laboratory test. 205. Presumption of unfitness to drive. 206. Power of pol

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 38
- Title: Motor Vehicles Amendment Act 2019
- Distance: 0.5628

**Retrieved passage:**

> tor cycle to be driven in contravention of the provisions of section 128 or the rules or regulations made thereunder shall be punishable with a fine of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194D. Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 129 or the rules or regulations made thereunder shall be punishable with a fine of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194E.Whoever while driving a motor vehicle fails to draw to the side of the road, on the approach of a fire service vehicle or of an ambulance or other emergency vehicle as may be specified by the State Government, shall be punishable with

## Question 2

**Question:** What is section 196 in my challan, driving without insurance?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 108
- Title: Motor Vehicles Act 1988
- Distance: 0.4352

**Retrieved passage:**

> 108 (b) drives a motor vehicle which makes use of a cut-out by which exhaust gases are released other than through the silencer, shall for the first contravention be issued a warning recorded in such manner as may be prescribed by the Central Government, and for any second or subsequent contravention shall be liable to penalty which shall not be less than one thousand rupees, but may extend to two thousand rupees.]] 195. [Imposition of minimum fine under certain circumstances.] Omitted by the Motor Vehicles (Amendment) Act, 2019 (32 of 2019), s. 80 (w.e.f. 1-9-2019). 196. Driving uninsured vehicle.—Whoever drives a motor vehicle or causes or allows a motor vehicle to be driven in contravention of the provisions of section 146 shall be 1[liable for the first contravention with penalty of th

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 9
- Title: Motor Vehicles Act 1988
- Distance: Not calculated

**Retrieved passage:**

> 9 SECTIONS 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders. 194D. Penalty for not wearing protective headgear. 194E. Failure to allow free passage to emergency vehicles. 194F. Use of horns and silence zones. 195. [Omitted]. 196. Driving uninsured vehicle. 197. Taking vehicle without authority. 198. Unauthorised interference with vehicle. 198A. Failure to comply with standards for road design, construction and maintenance. 199. Offences by companies. 199A. Offences by juveniles. 199B. Revision of fines and penalties. 200. Composition of certain offences. 201. Penalty for causing obstruction to free flow of traffic. 202. Power to arrest without warrant. 203. Breath tests. 204. Laboratory test. 205. Presumption of unfitness to drive. 206. Power of pol

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 39
- Title: Motor Vehicles Amendment Act 2019
- Distance: Not calculated

**Retrieved passage:**

> , consultant or concessionaire responsible under sub-section (1) to comply with standards for road design, construction and maintenance, results in death or disability, such authority or contractor or concessionaire shall be punishable with a fine which may extend to one lakh rupees and the same shall be paid to the Fund constituted under section 164B. (3) For the purposes of sub-section (2), the court shall in particular have regard to the following matters, namely:— (a) the characteristics of the road, and the nature and type of traffic which was reasonably expected to use it as per the design of road; (b) the standard of maintenance norms applicable for a road of that character and use by such traffic; Omission of section 195. Amendment of section 196. Amendment of section 197. Amendmen

## Question 3

**Question:** Under which section can the police seize my driving licence on the spot?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 113
- Title: Motor Vehicles Act 1988
- Distance: 0.3587

**Retrieved passage:**

> , 185, 189, 190, 194C, 194D, or 194E, seize the driving licence held by such driver and forward it to the licensing authority for disqualification or revocation proceedings under section 19: Provided that the person seizing the licence shall give to the person surrendering the licence a temporary acknowledgement therefor, but such acknowledgement shall not authorise the holder to drive until the licence has been returned to him.] 207. Power to detain vehicles used without certificate of registration permit, etc.—(1) Any police officer or other person authorised in this behalf by the State Government may, if he has reason to believe that a motor vehicle has been or is being used in contravention of the provisions of section 3 or section 4 or section 39 or without the permit required by sub-

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 113
- Title: Motor Vehicles Act 1988
- Distance: 0.3727

**Retrieved passage:**

> 113 document within the meaning of section 464 of the Indian Penal Code (45 of 1860), seize the mark or document and call upon the driver or owner of the vehicle to account for his possession of or the presence in the vehicle of such mark or document. (2) Any police officer or other person authorised in this behalf by the State Government may, if he has reason to believe that the driver of a motor vehicle who is charged with any offence under this Act may abscond or otherwise avoid the service of a summons, seize any licence held by such driver and forward it to the Court taking cognizance of the offence and the said Court shall on the first appearance of such driver before it, return the licence to him in exchange for the temporary acknowledgment given under sub-section (3). (3) A police 

### Result 3

- Source: `maharashtra_motor_vehicles_rules_1989.pdf`
- PDF page: 5
- Title: Maharashtra Motor Vehicles Rules 1989
- Distance: 0.3944

**Retrieved passage:**

> icensing authority shall remove the old photograph from the driving licence and affix and seal thereto one copy of the new photograph and return the driving licence to the applicant and shall, if he is not the licensing authority by whom the driving licence was issued, forward the second copy of the photograph to that authority : Provided that, if the holder of the driving licence so desires, the licensing authority shall issue a duplicate driving licence on payment of a fee of ‘(hundred rupees] with the new photograph affixed thereto and shall destroy the original driving licence. In such a case if the licensing authority is not the authority by whom the driving licence was issued he shall inform the original licensing authority. (4) When a new photograph is affixed to a driving licence a

## Question 4

**Question:** I got challan for no helmet and no insurance together, what is the total maximum fine?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 107
- Title: Motor Vehicles Act 1988
- Distance: 0.4926

**Retrieved passage:**

> o be driven with a child who, not having attained the age of fourteen years, is not secured by a safety belt or a child restraint system shall be 4[liable for a penalty] of one thousand rupees. 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders.— Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 128 or the rules or regulations made thereunder shall be 4[liable for a penalty] of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194D. Penalty for not wearing protective headgear.—Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 129 or the rules or regulations made

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 80
- Title: Motor Vehicles Act 1988
- Distance: 0.5054

**Retrieved passage:**

> 80 Provided further that the Central Government may by rules provide for measures for the safety of children below four years of age riding or being carried on a motorcycle. Explanation.— “Protective headgear” means a helmet which,— (a) by virtue of its shape, material and construction, could reasonably be expected to afford to the person driving or riding on a motorcycle a degree of protection from injury in the event of an accident; and (b) is securely fastened to the head of the wearer by means of straps or other fastenings provided on the headgear.] 130. Duty to produce licence and certificate of registration.—(1) The driver of a motor vehicle in any public place shall, on demand by any police officer in uniform, produce his licence for examination: Provided that the driver may, if his

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 38
- Title: Motor Vehicles Amendment Act 2019
- Distance: 0.5224

**Retrieved passage:**

> with a fine of two hundred rupees per excess passenger: Provided that such transport vehicle shall not be allowed to move before the excess passengers are off-loaded and an alternative transport is arranged for such passengers. 194B. (1) Whoever drives a motor vehicle without wearing a safety belt or carries passengers not wearing seat belts shall be punishable with a fine of one thousand rupees: Provided that the State Government, may by notification in the Official Gazette, exclude the application of this sub-section to transport vehicles to carry standing passengers or other specified classes of transport vehicles. (2) Whoever drives a motor vehicle or causes or allows a motor vehicle to be driven with a child who, not having attained the age of fourteen years, is not secured by a safet

## Question 5

**Question:** My son is 16 and drove the scooty, what penalty for him and for me as the owner?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 107
- Title: Motor Vehicles Act 1988
- Distance: 0.4377

**Retrieved passage:**

> o be driven with a child who, not having attained the age of fourteen years, is not secured by a safety belt or a child restraint system shall be 4[liable for a penalty] of one thousand rupees. 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders.— Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 128 or the rules or regulations made thereunder shall be 4[liable for a penalty] of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194D. Penalty for not wearing protective headgear.—Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 129 or the rules or regulations made

### Result 2

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 38
- Title: Motor Vehicles Amendment Act 2019
- Distance: 0.4630

**Retrieved passage:**

> with a fine of two hundred rupees per excess passenger: Provided that such transport vehicle shall not be allowed to move before the excess passengers are off-loaded and an alternative transport is arranged for such passengers. 194B. (1) Whoever drives a motor vehicle without wearing a safety belt or carries passengers not wearing seat belts shall be punishable with a fine of one thousand rupees: Provided that the State Government, may by notification in the Official Gazette, exclude the application of this sub-section to transport vehicles to carry standing passengers or other specified classes of transport vehicles. (2) Whoever drives a motor vehicle or causes or allows a motor vehicle to be driven with a child who, not having attained the age of fourteen years, is not secured by a safet

### Result 3

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 110
- Title: Motor Vehicles Act 1988
- Distance: 0.4672

**Retrieved passage:**

> venile has attained the age of twenty-five years. (6) Where an offence under this Act has been committed by a juvenile, then such juvenile shall be punishable with such fines as provided in the Act while any custodial sentence may be modified as per the provisions of the Juvenile Justice Act, 2000 (56 of 2000). 199B. Revision of fines 1[and penalties].—2[The fines and penalties] as provided in this Act shall be increased by such amount not exceeding ten per cent. in value of the existing fines, on an annual basis on 1st day of April of each year from the date of commencement of the Motor Vehicles (Amendment) Act, 2019 (32 of 2019), as may be notified by the Central Government.] 200. Composition of certain offences.—3[(1) Any offence whether committed before or after the commencement of thi

## Question 6

**Question:** Can I pay my Maharashtra e-challan at Kopargaon police station on Sunday?

### Result 1

- Source: `maharashtra_motor_vehicles_rules_1989.pdf`
- PDF page: 177
- Title: Maharashtra Motor Vehicles Rules 1989
- Distance: 0.5034

**Retrieved passage:**

> CHAPTER X MISCELLANEOUS 284. Refunds. – (l) If the Transport Commissioner, Maharashtra State or the Regional Transport Officer concerned. as the case may be, is satisfied that a refund is due on the ground that,- (a) it is admissible under sub-rule (3) of Rule 24 or sub-rule [1] of Rule 40; (b) wherever there is a provision that if the appellant succeeds in appeal, he is entitled to get the refund of fees in whole or any part; or (c) it represents the amount paid in excess or erroneously towards the fees under these rules in cash, cheque, demand draft, money order, into the Government Treasury by way of motor vehicles fee stamp; he shall issue to the person entitled to the refund of such amount, a certificate in Form RF of the First Schedule appended to these rules. (2) Any person to whom 

### Result 2

- Source: `maharashtra_motor_vehicles_rules_1989.pdf`
- PDF page: 24
- Title: Maharashtra Motor Vehicles Rules 1989
- Distance: 0.5168

**Retrieved passage:**

> succeeds, the Transport Commissioner Maharashtra State, or the registering authority concerned, as the case may be, may refund the fees in whole or in part, as he thinks fit (2) The appellate authority, after giving an opportunity to the parties to be heard and after such further enquiry, if any, as it may deem necessary may confirm, vary or set aside the order of the registering authority or the Inspector of Motor Vehicles or the Police Officer. as the case may be and shall make an order accordingly. (3) Any person preferring an appeal under the provisions of Chapter IV of the Act shall be entitled to obtain a copy of any document filed with the registering authority in connection with any order against which he is preferring an appeal on the payment of a fee calculated at the rate of [tw

### Result 3

- Source: `maharashtra_motor_vehicles_rules_1989.pdf`
- PDF page: 169
- Title: Maharashtra Motor Vehicles Rules 1989
- Distance: 0.5286

**Retrieved passage:**

> ard of compensation. NOTES Sub-rule (3) of rule 260 of the Maharashtra Motor Vehicles Rules, 1989 requires notice to be given to the Tribunal in respect of the claim or compensation under section 140 to the owner and insurer and there is no need to give notice to the driver.- Rama Kondiba Khade v. Sk. Sakir s/o Sk. Kachru, 2004 (1) Mah. L. J. 971. Decree or Award can be made personally against the driver of the offending vehicle if he is involved in a Claim Petition either as party or at least as witness.- The provisions of Rule 260 (1) and (2) of the Maharashtra Motor Vehicles Rules, 1989 are mandatory and are required to be followed by the Claims Tribunal to involve the owner, driver and insurer of the vehicle in question, in the manner prescribed. The Claims Tribunal has to pass an awar

## Question 7

**Question:** I received a challan under Section 183 for speeding. What is the maximum fine?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 102
- Title: Motor Vehicles Act 1988
- Distance: 0.4687

**Retrieved passage:**

> 102 Chapter VII or the rules and regulations made thereunder shall be punishable with imprisonment for a term which may extend to one year or with fine of one lakh rupees per such component or with both. (4) Whoever, being the owner of a motor vehicle, alters a motor vehicle, including by way of retrofitting of motor vehicle parts, in a manner not permitted under the Act or the rules and regulations made thereunder shall be punishable with imprisonment for a term which may extend to six months, or with fine of five thousand rupees per such alteration or with both. 182B. 1[Penalty] for contravention of section 62A.—Whoever contravenes the provisions of section 62A, shall be 2[liable for a penalty] which shall not be less than five thousand rupees, but may extend to ten thousand rupees.] 183

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 8
- Title: Motor Vehicles Act 1988
- Distance: 0.4833

**Retrieved passage:**

> uthorised persons to drive vehicles. 181. Driving vehicles in contravention of section 3 or section 4. 182. Offences relating to licences. 182A. Punishment for offences relating to construction, maintenance, sale and alteration of motor vehicles and components. 182B. Penalty for contravention of section 62A. 183. Driving at excessive speed, etc. 184. Driving dangerously. 185. Driving by a drunken person or by a person under the influence of drugs. 186. Driving when mentally or physically unfit to drive. 187. Punishment for offences relating to accident. 188. Punishment for abetment of certain offences. 189. Racing and trials of speed. 190. Using vehicle in unsafe condition. 191. [Omitted]. 192. Using vehicle without registration. 192A. Using vehicle without permit. 192B. Offences relating 

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 33
- Title: Motor Vehicles Amendment Act 2019
- Distance: 0.4859

**Retrieved passage:**

>  (a) after the words “Whoever drives”, the words “or causes any person who is employed by him or subjects someone under his control to drive” shall be inserted; (b) for the words "with fine which extend to four hundred rupees, or, if having been previously convicted of an offence under this sub-section is again Amendment of section 180. Amendment of section 181. Amendment of section 182. Substitution of new section for section 182A. Punishment for offences relating to construction, maintenance, sale and alteration of motor vehicles and components. Punishment for contravention of section 62A. Amendment of section 183. 1409070/2020/MVL Section 34

## Question 8

**Question:** What happens if I am caught drunk driving for the second time under Section 185?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 103
- Title: Motor Vehicles Act 1988
- Distance: 0.4170

**Retrieved passage:**

> 103 1[Explanation.—For the purpose of this section,— (a) jumping a red light; (b) violating a stop sign; (c) use of handheld communications devices while driving; (d) passing or overtaking other vehicles in a manner contrary to law; (e) driving against the authorised flow of traffic; or (f) driving in any manner that falls far below what would be expected of a competent and careful driver and where it would be obvious to a competent and careful driver that driving in that manner would be dangerous, shall amount to driving in such manner which is dangerous to the public.] 185. Driving by a drunken person or by a person under the influence of drugs.—Whoever, while driving, or attempting to drive, a motor vehicle,— 2[(a) has, in his blood, alcohol exceeding 30 mg. per 100 ml. of blood detecte

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 8
- Title: Motor Vehicles Act 1988
- Distance: Not calculated

**Retrieved passage:**

> uthorised persons to drive vehicles. 181. Driving vehicles in contravention of section 3 or section 4. 182. Offences relating to licences. 182A. Punishment for offences relating to construction, maintenance, sale and alteration of motor vehicles and components. 182B. Penalty for contravention of section 62A. 183. Driving at excessive speed, etc. 184. Driving dangerously. 185. Driving by a drunken person or by a person under the influence of drugs. 186. Driving when mentally or physically unfit to drive. 187. Punishment for offences relating to accident. 188. Punishment for abetment of certain offences. 189. Racing and trials of speed. 190. Using vehicle in unsafe condition. 191. [Omitted]. 192. Using vehicle without registration. 192A. Using vehicle without permit. 192B. Offences relating 

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 34
- Title: Motor Vehicles Amendment Act 2019
- Distance: Not calculated

**Retrieved passage:**

>  red light; (b) violating a stop sign; (c) use of handheld communications devices while driving; (d) passing or overtaking other vehicles in a manner contrary to law; (e) driving against the authorised flow of traffic; or (f) driving in any manner that falls far below what would be expected of a competent and careful driver and where it would be obvious to a competent and careful driver that driving in that manner would be dangerous, shall amount to driving in such manner which is dangerous to the public.”. 68. In section 185 of the principal Act,— (i) in clause (a), after the words “breath analyser,”, the words “or in any other test including a laboratory test,” shall be inserted; Amendment of section 184. Amendment of section 185. 1409070/2020/MVL Section 35

## Question 9

**Question:** My challan mentions Section 184. What does dangerous driving mean, and what additional punishment can apply?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 102
- Title: Motor Vehicles Act 1988
- Distance: 0.3997

**Retrieved passage:**

> nless that opinion is shown to be based on an estimate obtained by the use of some mechanical 6[or electronic] device. (4) The publication of a time table under which, or the giving of any direction that, any journey or part of a journey is to be completed within a specified time shall, if in the opinion of the Court it is not practicable in the circumstances of the case for that journey or part of a journey to be completed in the specified time without contravening the speed limits referred to in section 112 be prima facie evidence that the person who published the time table or gave the direction has committed an offence punishable under 7[sub-section (1)]. 184. Driving dangerously.—Whoever, drives a motor vehicle at a speed or in a manner which is dangerous to the public 8[or which caus

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 8
- Title: Motor Vehicles Act 1988
- Distance: 0.3843

**Retrieved passage:**

> uthorised persons to drive vehicles. 181. Driving vehicles in contravention of section 3 or section 4. 182. Offences relating to licences. 182A. Punishment for offences relating to construction, maintenance, sale and alteration of motor vehicles and components. 182B. Penalty for contravention of section 62A. 183. Driving at excessive speed, etc. 184. Driving dangerously. 185. Driving by a drunken person or by a person under the influence of drugs. 186. Driving when mentally or physically unfit to drive. 187. Punishment for offences relating to accident. 188. Punishment for abetment of certain offences. 189. Racing and trials of speed. 190. Using vehicle in unsafe condition. 191. [Omitted]. 192. Using vehicle without registration. 192A. Using vehicle without permit. 192B. Offences relating 

### Result 3

- Source: `motor_vehicles_amendment_act_2019.pdf`
- PDF page: 34
- Title: Motor Vehicles Amendment Act 2019
- Distance: Not calculated

**Retrieved passage:**

>  red light; (b) violating a stop sign; (c) use of handheld communications devices while driving; (d) passing or overtaking other vehicles in a manner contrary to law; (e) driving against the authorised flow of traffic; or (f) driving in any manner that falls far below what would be expected of a competent and careful driver and where it would be obvious to a competent and careful driver that driving in that manner would be dangerous, shall amount to driving in such manner which is dangerous to the public.”. 68. In section 185 of the principal Act,— (i) in clause (a), after the words “breath analyser,”, the words “or in any other test including a laboratory test,” shall be inserted; Amendment of section 184. Amendment of section 185. 1409070/2020/MVL Section 35

## Question 10

**Question:** I received a challan with Sections 194D and 196. Can ChalanCheck explain both violations separately?

### Result 1

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 107
- Title: Motor Vehicles Act 1988
- Distance: Not calculated

**Retrieved passage:**

> o be driven with a child who, not having attained the age of fourteen years, is not secured by a safety belt or a child restraint system shall be 4[liable for a penalty] of one thousand rupees. 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders.— Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 128 or the rules or regulations made thereunder shall be 4[liable for a penalty] of one thousand rupees and he shall be disqualified for holding licence for a period of three months. 194D. Penalty for not wearing protective headgear.—Whoever drives a motor cycle or causes or allows a motor cycle to be driven in contravention of the provisions of section 129 or the rules or regulations made

### Result 2

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 108
- Title: Motor Vehicles Act 1988
- Distance: Not calculated

**Retrieved passage:**

> 108 (b) drives a motor vehicle which makes use of a cut-out by which exhaust gases are released other than through the silencer, shall for the first contravention be issued a warning recorded in such manner as may be prescribed by the Central Government, and for any second or subsequent contravention shall be liable to penalty which shall not be less than one thousand rupees, but may extend to two thousand rupees.]] 195. [Imposition of minimum fine under certain circumstances.] Omitted by the Motor Vehicles (Amendment) Act, 2019 (32 of 2019), s. 80 (w.e.f. 1-9-2019). 196. Driving uninsured vehicle.—Whoever drives a motor vehicle or causes or allows a motor vehicle to be driven in contravention of the provisions of section 146 shall be 1[liable for the first contravention with penalty of th

### Result 3

- Source: `motor_vehicles_act_1988.pdf`
- PDF page: 9
- Title: Motor Vehicles Act 1988
- Distance: Not calculated

**Retrieved passage:**

> 9 SECTIONS 194C. Penalty for violation of safety measures for motor cycle drivers and pillion riders. 194D. Penalty for not wearing protective headgear. 194E. Failure to allow free passage to emergency vehicles. 194F. Use of horns and silence zones. 195. [Omitted]. 196. Driving uninsured vehicle. 197. Taking vehicle without authority. 198. Unauthorised interference with vehicle. 198A. Failure to comply with standards for road design, construction and maintenance. 199. Offences by companies. 199A. Offences by juveniles. 199B. Revision of fines and penalties. 200. Composition of certain offences. 201. Penalty for causing obstruction to free flow of traffic. 202. Power to arrest without warrant. 203. Breath tests. 204. Laboratory test. 205. Presumption of unfitness to drive. 206. Power of pol
