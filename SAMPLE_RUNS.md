# Sample runs

Generated 2026-11-10 against http://127.0.0.1:8000 by `uv run sample_runs.py http://127.0.0.1:8000`.


## 1. Since 2020, have FDA reports of pancreatitis for semaglutide (Ozempic, Wegovy) grown faster than the number of Medicare patients taking it, and does its official FDA label warn about pancreatitis?

### Expected (computed directly from openFDA, no model)

US reports listing PANCREATITIS, by year received: 2020: 143 US reports / 297,488 Medicare users = 48.1 per 100k; 2021: 126 US reports / 566,867 Medicare users = 22.2 per 100k; 2022: 120 US reports / 964,868 Medicare users = 12.4 per 100k; 2023: 150 US reports / 1,750,208 Medicare users = 8.6 per 100k; 2024: 225 US reports / 2,315,591 Medicare users = 9.7 per 100k. Pancreatitis on the current label: yes.

Source: `/drug/event.json` count by receivedate (https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate), `data/medicare_part_d_users.csv` (CMS Medicare Part D Spending by Drug) and `/drug/label.json` (https://api.fda.gov/drug/label.json?search=openfda.generic_name%3A%22semaglutide%22&limit=20)

### This agent

**Short answer:** No, FDA reports of pancreatitis for semaglutide have not grown faster than the number of Medicare patients taking the drug ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug), [FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)). While the number of Medicare patients using semaglutide grew significantly between 2020 and 2024, the rate of US pancreatitis reports per 100,000 Medicare users actually decreased over this same period ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug), [FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)). However, the drug's official FDA label—which is the official prescribing information that comes with the drug and lists its known risks—does explicitly warn about pancreatitis ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).

---

### Medicare Users vs. US Pancreatitis Reports

Since 2020, the number of Medicare Part D patients prescribed semaglutide (which includes Ozempic, Rybelsus, and Wegovy) has risen from under 300,000 to over 2.3 million ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)). During this same timeframe, US-based side-effect reports of pancreatitis did not grow at the same pace, causing the report rate per 100,000 users to drop from 48.1 in 2020 down to 9.7 in 2024 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)).

| Year | Total Medicare Users | US Pancreatitis Reports | Reports per 100,000 Users |
| :--- | :--- | :--- | :--- |
| **2020** | 297,488 ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)) | 143 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) | 48.1 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) |
| **2021** | 566,867 ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)) | 126 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) | 22.2 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) |
| **2022** | 964,868 ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)) | 120 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) | 12.4 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) |
| **2023** | 1,750,208 ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)) | 150 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) | 8.6 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) |
| **2024** | 2,315,591 ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)) | 225 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) | 9.7 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) |

### Total Worldwide FAERS Reports

Looking globally, the total number of pancreatitis reports submitted to the FDA's Adverse Event Reporting System (FAERS) for semaglutide by year are ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate)):
* **2020:** 164 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2021:** 159 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2022:** 160 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2023:** 249 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2024:** 393 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2025:** 356 reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))
* **2026:** 218 reports *(noted as a partial year)* ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22&count=receivedate))

### FDA Label Warnings

Yes, the FDA-approved label for Ozempic contains several detailed warnings regarding pancreatitis ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)):
* **Warnings Section:** Pancreatitis is marked as present in key warning sections ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Warnings and Precautions (Section 5.2):** This section specifically lists acute pancreatitis as being observed in patients treated with GLP-1 receptor agonists, including Ozempic, and instructs providers to discontinue the drug immediately if pancreatitis is suspected ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Adverse Reactions:** It is listed as a serious adverse reaction ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Patient Materials:** Both the Medication Guide and Patient Information sections warn patients about pancreatitis and describe symptoms, such as severe abdominal pain radiating to the back, instructing patients to stop taking the medication and seek immediate medical care if these symptoms occur ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Patient Information:** This section instructs healthcare providers to inform patients of the potential for acute pancreatitis and its symptoms ([label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).

---

### What this data can't tell you

The side-effect reports from the FAERS database represent spontaneous submissions and do not prove that semaglutide caused the pancreatitis. Because FAERS does not track the total number of people taking semaglutide worldwide, it is impossible to calculate a true overall reporting rate from FAERS reports alone. While we can estimate a reporting rate using Medicare data, this serves only as a rough index for Medicare Part D patients and may not accurately reflect the rate for younger or non-Medicare patients. Furthermore, side-effect reporting is known to fluctuate or rise when a drug receives significant news coverage. Finally, the data utilized in this report does not contain information regarding drug recalls, nor does it provide a full comparison of pancreatitis report rates specifically for Wegovy versus Ozempic users in the earlier years.

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 9 tool calls, 4 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "semaglutide"}` |
| Lead | `research` | `{"task": "FDA FAERS reports of pancreatitis for semaglutide by year since 2020"}` |
| Lead | `research` | `{"task": "Medicare Part D patient counts for semaglutide by year since 2020"}` |
| Lead | `research` | `{"task": "Use faers_report_rate to get pancreatitis reports per 100,000 Medicare users for semaglutide by year since 202` |
| Lead | `research` | `{"task": "FDA label warnings for pancreatitis on semaglutide"}` |
| Researcher 4 | `label_warnings` | `{"drug": "semaglutide", "find": "pancreatitis"}` |
| Researcher 2 | `medicare_users` | `{"drug": "semaglutide"}` |
| Researcher 1 | `faers_trend` | `{"reaction": "PANCREATITIS", "drug": "semaglutide"}` |
| Researcher 3 | `faers_report_rate` | `{"drug": "semaglutide", "reaction": "PANCREATITIS"}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

To answer your questions accurately, we must look at the data regarding Medicare enrollment, FDA adverse event reporting, and the official prescribing information for semaglutide. 

Here is the breakdown of how these trends compare and what the official FDA labels state.

---

### Part 1: Have FDA reports of pancreatitis grown faster than Medicare usage since 2020?

There is no scientific or epidemiological evidence showing that FDA reports of pancreatitis have grown *faster* than the rate of patient uptake (including among Medicare beneficiaries). In fact, the data suggests the opposite: the growth in prescriptions has been so massive that it far outpaces the relative rate of reporting for this specific side effect.

Here is why a direct comparison is complex, along with the key data points:

#### 1. The Explosion in Medicare Usage
The number of Medicare patients prescribed semaglutide has grown at an unprecedented, exponential rate since 2020. 
* According to analysis by the **Kaiser Family Foundation (KFF)**, the number of Medicare Part D enrollees using Ozempic grew from approximately **225,000 in 2020** to more than **1.2 million by 2023**—an increase of over 400% in just three years. 
* Total Medicare spending on these drugs skyrocketed from under $1 billion to several billion dollars annually during this period.

#### 2. FDA Adverse Event Reporting System (FAERS) Trends
While the *absolute number* of pancreatitis reports submitted to the FDA for semaglutide has increased since 2020, this is expected. In pharmacovigilance, as the "denominator" (the total number of people taking a drug) grows into the millions, the "numerator" (the number of reported side effects) will naturally rise.
* **The "Weber Effect":** When a drug becomes highly publicized (as Ozempic and Wegovy did in 2022 and 2023), spontaneous reporting of side effects by doctors and patients typically spikes. 
* Despite this spike in absolute reports, epidemiologic studies (such as those published in *JAMA* in late 2023) show that while the risk of pancreatitis is higher for GLP-1 drugs than for other weight-loss drugs, the **overall absolute risk remains very low** (approximately 4 to 5 cases per 1,000 patient-years). 

**In summary:** Because Medicare (and general population) usage of semaglutide grew from a relatively small base in 2020 to an absolute blockbuster status by 2023/2024, the rate of prescription growth has dramatically outpaced the underlying rate of pancreatitis reporting.

---

### Part 2: Does the official FDA label warn about pancreatitis?

**Yes.** The official FDA-approved prescribing information for all semaglutide products—**Ozempic, Wegovy, and Rybelsus**—contains explicit warnings about the risk of pancreatitis.

#### What the Labels Say:
* **Section 5 (Warnings and Precautions):** Under **"Acute Pancreatitis,"** the labels state that acute pancreatitis (including fatal and non-fatal hemorrhagic or necrotizing pancreatitis) has been observed in patients treated with GLP-1 receptor agonists, including semaglutide, during clinical trials and post-marketing surveillance.
* **Instructions to Providers:** The labels instruct healthcare providers to monitor patients for signs of pancreatitis—specifically, **severe, persistent abdominal pain** that may radiate to the back and may be accompanied by vomiting. 
* **Action Plan:** If pancreatitis is suspected, providers are instructed to immediately discontinue semaglutide and initiate appropriate management. If pancreatitis is confirmed, semaglutide should not be restarted. 

Additionally, the **Patient Counseling Information** and the **Medication Guide** provided to patients with their prescriptions explicitly list "inflammation of the pancreas (pancreatitis)" as a serious potential side effect and advise them to seek immediate medical help if they experience severe stomach pain.


## 2. Compare semaglutide, tirzepatide and liraglutide: what share of each drug's FDA adverse event reports mention suicidal ideation?

### Expected (computed directly from openFDA, no model)

semaglutide: 520 of 78023 reports (0.67%); tirzepatide: 509 of 181068 reports (0.28%); liraglutide: 169 of 51303 reports (0.33%).

Source: `/drug/event.json` report totals, with and without `patient.reaction.reactionmeddrapt:"SUICIDAL IDEATION"`

### This agent

**Short answer:** Semaglutide has the highest share of suicidal ideation reports, with 0.7% of its total side-effect reports mentioning this issue ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)). Both tirzepatide and liraglutide have a lower share, with suicidal ideation mentioned in 0.3% of their reports ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)). Official safety warnings on drug packaging vary depending on the specific brand name and have changed recently ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).

---

### Share of Adverse Event Reports Mentioning Suicidal Ideation

According to the FDA Adverse Event Reporting System (FAERS), semaglutide has the highest percentage of reports mentioning suicidal ideation among the three drugs, though the overall percentages remain low for all of them ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)). 

| Drug | Total Reports | Suicidal Ideation Reports | Share of Total Reports |
| :--- | :--- | :--- | :--- |
| **Semaglutide** | 78,023 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 520 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 0.7% ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) |
| **Tirzepatide** | 181,068 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 509 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 0.3% ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) |
| **Liraglutide** | 51,303 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 169 ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) | 0.3% ([FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)) |

---

### FDA Label Warnings and Precautions

The FDA label is the official prescribing information that comes with the drug and lists its known risks ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)). Because these active ingredients are sold under different brand names for different uses (such as diabetes or weight loss), the warnings listed on their labels can vary ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)):

*   **Semaglutide:** The label for Ozempic does not contain warnings for suicidal ideation ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)). However, the Wegovy label (dated April 23, 2024) does include suicidal behavior and ideation in its warnings, precautions, adverse reactions, and patient guidelines ([DailyMed Wegovy](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f5e548d0-cc79-4c34-a3f5-e20a5b8b6564)).
*   **Tirzepatide:** The Mounjaro label (dated August 27, 2026) does not list suicidal ideation warnings ([DailyMed Mounjaro](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d2d7da5d-ad07-4228-955f-cf7e355c8cc0)). The Zepbound label previously had warnings for "Suicidal Behavior and Ideation," but this warning was officially removed in February 2026 ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=487cd7e7-434c-4925-99fa-aa80b1cc776b)).
*   **Liraglutide:** The evaluated generic Meitheal Pharmaceuticals label does not contain suicidal ideation warnings ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0efc3a89-211a-4496-baab-e8265e07de2b)). The Saxenda label previously included warnings for suicidal behavior and ideation, but this warning was removed in February 2026 ([DailyMed Saxenda](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=3946d389-0926-4f77-a708-0acb8153b143)).

---

### FDA Drug Recalls Since 2020

Drug recalls represent actions taken to remove specific batches of a drug from the market due to safety or quality issues ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22semaglutide%22+OR+openfda.brand_name%3A%22semaglutide%22+OR+product_description%3A%22semaglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)).

*   **Semaglutide:** Had 57 total Class II recalls since 2020 ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22semaglutide%22+OR+openfda.brand_name%3A%22semaglutide%22+OR+product_description%3A%22semaglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). The primary reason was sterility or manufacturing practice problems (30 recalls) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22semaglutide%22+OR+openfda.brand_name%3A%22semaglutide%22+OR+product_description%3A%22semaglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). Recalls occurred across multiple years, peaking in 2025 (23 recalls) and 2026 (19 recalls) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22semaglutide%22+OR+openfda.brand_name%3A%22semaglutide%22+OR+product_description%3A%22semaglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)).
*   **Tirzepatide:** Had 28 total recalls (1 Class I and 27 Class II) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22tirzepatide%22+OR+openfda.brand_name%3A%22tirzepatide%22+OR+product_description%3A%22tirzepatide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). The primary reason was sterility or manufacturing practice problems (19 recalls) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22tirzepatide%22+OR+openfda.brand_name%3A%22tirzepatide%22+OR+product_description%3A%22tirzepatide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). Most occurred in 2025 (14 recalls) and 2026 (9 recalls) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22tirzepatide%22+OR+openfda.brand_name%3A%22tirzepatide%22+OR+product_description%3A%22tirzepatide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)).
*   **Liraglutide:** Had 4 total recalls (1 Class I and 3 Class II) ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22liraglutide%22+OR+openfda.brand_name%3A%22liraglutide%22+OR+product_description%3A%22liraglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). Three recalls were due to storage temperature problems ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22liraglutide%22+OR+openfda.brand_name%3A%22liraglutide%22+OR+product_description%3A%22liraglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)). Three occurred in 2021 and one occurred in 2026 ([recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22liraglutide%22+OR+openfda.brand_name%3A%22liraglutide%22+OR+product_description%3A%22liraglutide%22%29+AND+recall_initiation_date%3A%5B20200101+TO+29991231%5D&limit=100)).

---

### What this data can't tell you

The safety data used in this report comes with several limitations:
*   **No proof of cause:** Side-effect reports submitted to the FDA (FAERS) only show that an event was reported after taking a drug. They do not prove that the drug actually caused the suicidal ideation.
*   **No user counts or risk rates:** FAERS does not track the total number of people taking each drug, meaning we cannot calculate the actual rate of risk. The percentage only shows what share of submitted *reports* mentioned suicidal ideation, not the likelihood of a patient experiencing it.
*   **Reporting biases:** Side-effect reporting often increases following news or media coverage about a potential issue.
*   **Recall limits:** A drug recall is usually restricted to a specific manufactured batch and is not proof that the drug itself harmed any patients. Additionally, older or smaller recalls may have named the drug differently, which might affect the counts.
*   **Unsearched labels:** This data does not include search results for every single brand-name formulation of these active ingredients, and warnings can vary across different brands.

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 17 tool calls, 4 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "semaglutide"}` |
| Lead | `resolve_drug_name` | `{"name": "tirzepatide"}` |
| Lead | `resolve_drug_name` | `{"name": "liraglutide"}` |
| Lead | `research` | `{"task": "Compare the share of FAERS reports mentioning suicidal ideation for semaglutide, tirzepatide, and liraglutide ` |
| Lead | `research` | `{"task": "Check FDA labels for semaglutide, tirzepatide, and liraglutide regarding suicidal ideation warnings or precaut` |
| Lead | `research` | `{"task": "Check FDA recalls for semaglutide, tirzepatide, and liraglutide"}` |
| Researcher 1 | `faers_compare_drugs` | `{"drugs": ["semaglutide", "tirzepatide", "liraglutide"], "reaction": "SUICIDAL IDEATION"}` |
| Researcher 2 | `label_warnings` | `{"find": "suicid", "drug": "semaglutide"}` |
| Researcher 2 | `label_warnings` | `{"find": "suicid", "drug": "tirzepatide"}` |
| Researcher 2 | `label_warnings` | `{"find": "suicid", "drug": "liraglutide"}` |
| Researcher 3 | `drug_recalls` | `{"drug": "semaglutide", "start_year": 2020}` |
| Researcher 3 | `drug_recalls` | `{"drug": "tirzepatide", "start_year": 2020}` |
| Researcher 3 | `drug_recalls` | `{"start_year": 2020, "drug": "liraglutide"}` |
| Lead | `research` | `{"task": "Check FDA labels for Wegovy, Saxenda, and Mounjaro regarding suicidal ideation warnings"}` |
| Researcher 4 | `label_warnings` | `{"drug": "Wegovy", "find": "suicid"}` |
| Researcher 4 | `label_warnings` | `{"find": "suicid", "drug": "Saxenda"}` |
| Researcher 4 | `label_warnings` | `{"drug": "Mounjaro", "find": "suicid"}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

While the FDA Adverse Event Reporting System (FAERS) is a constantly updating database, independent pharmacovigilance studies and regulatory audits show that reports of suicidal ideation make up an extremely small fraction of the total reported adverse events for semaglutide, tirzepatide, and liraglutide—typically **well under 0.5% (or 1 in 200 to 1 in 1,000 of all submitted reports)** for each drug.

Because FAERS relies on voluntary reporting, these numbers represent *reported associations*, not proof of causation. Below is a comparison of how these three drugs compare regarding suicidal ideation reports, the context of the data, and the official findings from regulatory agencies.

---

### 1. Semaglutide (Ozempic, Wegovy, Rybelsus)
* **Estimated Share of Reports:** **~0.2% to 0.4%** of total FAERS reports.
* **Context:** Semaglutide has been subject to intense media scrutiny since late 2022. This led to a phenomenon known as "stimulated reporting," where news coverage prompts patients and doctors to file reports they otherwise might not have. Despite this spike in raw volume, the proportion of reports mentioning suicidal thoughts remains incredibly low. Out of tens of thousands of adverse event reports filed for semaglutide, only a few hundred mention suicidal ideation or self-harming behavior.

### 2. Liraglutide (Victoza, Saxenda)
* **Estimated Share of Reports:** **~0.1% to 0.3%** of total FAERS reports.
* **Context:** Liraglutide is an older, first-generation daily GLP-1 receptor agonist approved in 2010 (Victoza) and 2014 (Saxenda). Because Saxenda was approved for weight loss, it carried a precautionary warning label for suicidal ideation from the beginning. (At the time, the FDA routinely mandated this warning for all weight-loss drugs due to psychiatric issues caused by older, unrelated anti-obesity drugs like rimonabant). Despite having over a decade of data, the proportion of reports remains extremely low.

### 3. Tirzepatide (Mounjaro, Zepbound)
* **Estimated Share of Reports:** **~0.1% to 0.2%** of total FAERS reports.
* **Context:** Tirzepatide is a dual GIP/GLP-1 receptor agonist approved more recently (2022 for diabetes, late 2023 for obesity). Because it has been on the market for less time, it has a lower total volume of FAERS reports overall. Within its database profile, reports of suicidal ideation are exceptionally rare, tracking at or slightly below the rates seen in semaglutide.

---

### What the Regulatory Agencies Found

Both the US Food and Drug Administration (FDA) and the European Medicines Agency (EMA) have conducted deep-dive reviews of these database reports to determine if the drugs actually cause suicidal thoughts. 

* **The FDA's Findings (January 2024):** After a detailed review of FAERS reports for all GLP-1 receptor agonists, the FDA stated that their reviews **"did not demonstrate a clear relationship between the use of these medicines and suicidal thoughts or actions."** The FDA noted that many reports had confounding factors (such as a history of depression or life stressors) that made a causal link highly unlikely.
* **The EMA's Findings (April 2024):** The European Medicines Agency’s Pharmacovigilance Risk Assessment Committee (PRAC) concluded a year-long investigation and stated that **the available evidence does not support a causal association** between GLP-1 receptor agonists and suicidal or self-harming thoughts or actions.

### Real-World Medical Records vs. FAERS Reports
To get past the limitations of FAERS (which can contain duplicate, unverified, or biased reports), researchers have analyzed actual electronic health records (EHRs). 

A landmark study funded by the National Institutes of Health (NIH) and published in *Nature Medicine* (January 2024) examined the health records of more than 1.8 million patients. The researchers found that **patients prescribed semaglutide actually had a *lower* risk of first-time and recurrent suicidal ideation** compared to patients prescribed non-GLP-1 medications for obesity or diabetes. 

### Summary
If you look at FAERS data, suicidal ideation accounts for a **tiny fraction of 1%** of all reported side effects for semaglutide, tirzepatide, and liraglutide. Large-scale clinical studies and federal reviews have repeatedly concluded that these medications do not show a causal link to suicidal thoughts, and may even be associated with a lower risk of psychiatric distress compared to other treatments.


## 3. Has metformin been recalled since 2019, and why?

### Expected (computed directly from openFDA, no model)

65 recall records since 2019. By reason: NDMA or other nitrosamine impurity: 47; Storage temperature problem: 6; Foreign material or wrong pill in the bottle: 5; Sterility or manufacturing practice problem: 4; Failed dissolution or potency test: 2; Other impurity or contamination: 1. By year started: 2020: 44, 2021: 15, 2022: 1, 2023: 1, 2024: 1, 2025: 2, 2026: 1.

Source: `/drug/enforcement.json` (https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)

### This agent

**Short answer:** Yes, metformin has been recalled 65 times since 2019 ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])). The most common reason for these recalls was the discovery of an impurity called NDMA or other nitrosamines ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])). Most of these recalls occurred in 2020 and 2021, and the majority were classified as Class II recalls ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])).

---

### Metformin Recalls and Reasons

Since 2019, there have been 65 total FDA drug recalls for metformin, including 62 Class II recalls and 3 Class III recalls ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])). 

The reasons for these recalls include ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])):

| Reason for Recall | Number of Recalls |
| :--- | :--- |
| NDMA or other nitrosamine impurity | 47 |
| Storage temperature problem | 6 |
| Foreign material or wrong pill in the bottle | 5 |
| Sterility or manufacturing practice problem | 4 |
| Failed dissolution or potency test | 2 |
| Other impurity or contamination | 1 |

Despite these recall actions, the FDA label—which is the official prescribing information that comes with the drug and lists its known risks—does not mention nitrosamines or NDMA in its warnings or sections as of September 9, 2026 ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=05999192-ebc6-4198-bd1e-f46abbfb4f8a)).

### Recalls by Year and Manufacturer

The recalls peaked sharply in 2020, with only a few occurring in the years since ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])):
* **2020:** 44 recalls ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2021:** 15 recalls ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2022:** 1 recall ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2023:** 1 recall ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2024:** 1 recall ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2025:** 2 recalls ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))
* **2026:** 1 recall ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231]))

The manufacturing firms associated with the 10 most recent listed recalls include Boehringer Ingelheim Pharmaceuticals, Inc., Glenmark Pharmaceuticals Inc., USA, A-S Medication Solutions LLC, Granules Pharmaceuticals Inc., Teva Pharmaceuticals USA Inc, Merck Sharp & Dohme Corp., RemedyRepack Inc., Viona Pharmaceuticals Inc., and Sun Pharmaceutical Industries Inc. ([openFDA Enforcement](https://api.fda.gov/drug/enforcement.json?search=(openfda.generic_name:%22metformin%22+OR+openfda.brand_name:%22metformin%22+OR+product_description:%22metformin%22)+AND+recall_initiation_date:[20190101+TO+29991231])).

### Side-Effect Reports by Year

The FDA Adverse Event Reporting System (FAERS) received the following numbers of side-effect reports mentioning metformin each year:
* **2019:** 34,692 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2020:** 32,301 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2021:** 27,598 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2022:** 26,840 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2023:** 26,631 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2024:** 25,382 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2025:** 25,605 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))
* **2026 (partial year):** 18,805 reports ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22metformin%22+OR+patient.drug.openfda.brand_name%3A%22metformin%22%29&count=receivedate))

---

### What this data can't tell you

The data in this report has several limitations:
* **Side-effect reports:** These reports do not prove that the drug caused the reported health problems. Because FAERS does not contain a count of the total number of people using the drug, there is no way to calculate an actual risk rate. Additionally, reporting rates can temporarily rise due to news coverage.
* **Recalls:** A recall is usually about a specific batch or lot of a medication; it is not proof that anyone was actually harmed. Older or smaller recalls may also use different names for the drug and may not be fully represented in these numbers.
* **Unanswered questions:** This data does not show whether any specific patients suffered injuries or long-term health consequences from taking the recalled batches of metformin.

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 9 tool calls, 3 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "metformin"}` |
| Lead | `research` | `{"task": "FDA recalls for metformin since 2019, including reasons for recalls and manufacturer names (FDA Recalls)"}` |
| Lead | `research` | `{"task": "FDA safety alerts, label changes, or warnings for metformin since 2019, particularly regarding nitrosamine (ND` |
| Lead | `research` | `{"task": "FAERS side-effect reports for metformin by year since 2019 (FAERS)"}` |
| Researcher 3 | `faers_trend` | `{"drug": "metformin", "reaction": ""}` |
| Researcher 1 | `drug_recalls` | `{"drug": "metformin", "start_year": 2019}` |
| Researcher 2 | `label_warnings` | `{"find": "nitrosamine", "drug": "metformin"}` |
| Researcher 2 | `label_warnings` | `{"drug": "metformin", "find": "NDMA"}` |
| Researcher 2 | `drug_recalls` | `{"drug": "metformin", "start_year": 2019}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

**Yes, metformin has been subject to multiple recalls since late 2019.** 

The recalls primarily occurred between **2020 and 2021**, though some isolated recalls extended into later years. 

Below is a detailed breakdown of why these recalls happened, which formulations were affected, and what patients should know.

---

### Why was Metformin recalled?
The recalls were triggered by the detection of **NDMA (N-Nitrosodimethylamine)** at levels exceeding the acceptable daily intake limit set by the U.S. Food and Drug Administration (FDA).

* **What is NDMA?** NDMA is a common environmental contaminant found in water and foods (such as cured meats, dairy products, and vegetables). 
* **The Risk:** It is classified as a **probable human carcinogen**, meaning exposure to high levels over a long period of time may increase the risk of cancer. 
* **The Cause:** The FDA determined that NDMA can form during the manufacturing process of the active pharmaceutical ingredient, or it can develop over time while the medication is sitting in storage or on pharmacy shelves.

---

### Which formulations were affected?
The recalls **almost exclusively affected Metformin Extended-Release (ER or XR)** formulations (specifically 500 mg and 750 mg tablets). 

* **Immediate-Release (IR) metformin**—the standard version of the drug taken multiple times a day—was **not** found to have high levels of NDMA and was not recalled. 
* Only specific lots from certain manufacturers were recalled, not all metformin ER on the market.

---

### Timeline of Key Recalls
* **Late 2019:** The FDA began investigating NDMA levels in metformin after regulatory agencies in other countries (like Singapore) detected the impurity.
* **May 2020:** The FDA announced that its laboratory testing had revealed NDMA levels above the acceptable limit in several lots of ER metformin and officially recommended that manufacturers recall these products.
* **2020–2021 (The Peak):** Numerous pharmaceutical companies voluntarily recalled specific lots of Metformin ER. Major manufacturers involved included:
  * **Amneal Pharmaceuticals**
  * **Apotex Corp.**
  * **Lupin Pharmaceuticals**
  * **Marksans Pharma**
  * **Teva Pharmaceuticals**
  * **Viona Pharmaceuticals**
  * **Nostrum Laboratories**
* **Late 2021–Present:** While the massive wave of recalls ended, occasional, isolated lot recalls have occurred as companies continue to test their batches. 

---

### What should you do if you take Metformin?
If you currently take metformin, healthcare professionals and the FDA advise the following:

1. **Do NOT stop taking your metformin abruptly.** Stopping your diabetes medication without a replacement can cause your blood sugar to spike to dangerous levels, posing an immediate and serious risk to your health (such as diabetic ketoacidosis or cardiovascular events). This risk is far greater than the theoretical, long-term risk of low-level NDMA exposure.
2. **Check your bottle.** Look at the label to find the manufacturer name and lot number. 
3. **Verify with your pharmacist or doctor.** You can check your specific medication against the [FDA's Metformin Recall List](https://www.fda.gov/drugs/drug-safety-and-availability/search-list-recalled-metformin-products). If your prescription is on the list, contact your pharmacy or doctor. They will provide a replacement batch from an unaffected manufacturer or switch you to an immediate-release formulation.
