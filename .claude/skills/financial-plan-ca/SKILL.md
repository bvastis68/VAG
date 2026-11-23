---
name: financial-plan-ca
description: Build or update a financial plan for a client household, scoped to that household's actual residency and citizenship. Covers retirement and decumulation projections, RESP education funding, estate and probate planning, corporate/Holdco integration, and cash flow analysis. Canadian-only households get Canadian rules only. Foreign rules load only where a real residency, citizenship or asset trigger fires. Use for new client onboarding, annual plan reviews, or scenario modeling in the Vastis practice. Triggers on "financial plan", "retirement plan", "can I retire", "decumulation", "RRSP meltdown", "OAS clawback", "RRIF minimum", "education funding", "RESP", "estate plan", "probate", "cash flow analysis", or "plan update".
---

# Financial Plan

Replaces the U.S.-default `financial-plan` skill for this practice. That skill
asks for 401(k), IRA and Social Security and models federal and state estate
tax. This one asks the questions that apply to the household in front of you.

Defer to `firm-context` for account taxonomy, house views, and style.

## Step 0: Scope the plan before anything else

**Run this gate first. It decides which rules exist for the rest of the plan.**

Establish, per person in the household, not per household:

1. Tax residency today. Which country, which province.
2. Citizenship, and any permanent residency or green card.
3. U.S. person status: citizen, green card holder, or meets the substantial
   presence test.
4. Assets situated outside the country of residence, with the country and the
   approximate cost amount.
5. Any planned change of residence in the plan horizon.

Then select exactly one track.

| Condition | Track |
|---|---|
| Every person is a Canadian resident, no one is a U.S. person, no foreign-situs assets, no planned move | **Track A** |
| Any one of those is false | **Track B**, loading only the triggers that fired |

### Hard rules on scope

- **Never infer status.** If residency, citizenship or U.S. person status is
  unknown, stop and ask. Do not assume Canadian-only because nothing was said,
  and do not add foreign content as a precaution. An unanswered gate question
  blocks the plan; it does not get a default.
- **Run the gate per person.** One spouse can be a U.S. person while the other
  is not. That household is Track B for that person and Track A for the other,
  and the interaction between them is itself a planning item.
- **Do not carry a trigger that did not fire.** A client with U.S.-situs stock
  but no U.S. personhood gets the situs rules and nothing else. No FBAR, no
  3520, no PFIC.
- **One reporting currency.** Report in the household's currency of residence,
  CAD for a Canadian resident. Add a second currency only where the client
  actually holds or spends in it. Never mix currencies inside one table. Where a
  conversion is used, state the rate and its date.
- **Record the determination in the plan** and re-run this gate at every annual
  review. Status moves: green cards get issued, day counts accumulate, people
  relocate.

## Input Discipline

A plan is only as honest as its inputs. Three rules:

1. **Never invent return, volatility or correlation assumptions.** Use RBC's
   current capital market assumptions, or assumptions the advisor supplies.
   State them in the plan.
2. **Never state an indexed figure from memory.** OAS recovery-tax threshold,
   TFSA and RRSP contribution limits, CPP/OAS maximums, YMPE, and the passive-
   income threshold are indexed or legislated and move. Confirm the current-year
   number before it goes in a deliverable. Mechanics are stable; the dollar
   figures are not.
3. **Monte Carlo means an actual simulation.** Run the computation. Do not
   produce a probability-of-success figure by estimation. If the inputs are not
   available, say so rather than producing a number.

---

# Track A: Canadian household

Use this when the gate returned Track A. Canadian rules only.

**What must not appear in a Track A plan.** These are not applicable caveats,
they are noise, and they make the plan read as generic:

- 401(k), IRA, Roth, Social Security
- FBAR, Form 8938, Form 3520 or 3520-A
- PFIC treatment of Canadian funds
- U.S. estate tax, lifetime exemption, prorated treaty credit
- Substantial presence test, closer connection
- T1135 foreign property reporting
- Any statement that a TFSA or RESP carries a foreign reporting problem

In a Track A plan a TFSA is simply a tax-free account and an RESP is simply an
education account. Say so plainly.

## A1: Client Profile

- **Demographics.** Ages, spouse age, dependants, province of residence, life
  expectancy assumption. Plan to 95 as default, longer for a healthy UHNW client.
- **Employment.** Income, bonus, expected raises, target retirement age,
  employer pension (DB or DC), business ownership.
- **Accounts**, with balances, allocation and contribution room:
  - RRSP and Spousal RRSP
  - RRIF, if already converted
  - TFSA
  - RESP, per beneficiary, with CESG received to date
  - LIRA and LIF
  - Non-registered
  - Corporate and Holdco
  - Trusts: family, alter-ego, joint-partner
- **Government benefits.** CPP or QPP statement of contributions. OAS
  eligibility and years of Canadian residence after 18.
- **Expenses.** Current spending and expected changes: mortgage payoff, children
  independent, care costs.
- **Liabilities.** Mortgage, investment loans, IFA facilities, corporate debt.
- **Insurance.** Life, personal and corporate-owned, disability, critical
  illness, long-term care.
- **Estate.** Wills, including separate wills for private-company shares where
  the province allows. POAs, beneficiary and successor-holder designations,
  gifting, philanthropic intent.

## A2: Cash Flow

| Year | Age | Employment Income | Investment Income | Taxes | Living Expenses | Savings | Net |
|------|-----|-------------------|-------------------|-------|-----------------|---------|-----|

- Inflation assumption, 2 to 3 percent default, higher for care costs.
- **Marginal rates by income type.** Canadian rates differ sharply across
  salary, eligible dividends, non-eligible dividends, capital gains and
  interest. Never blend them into one effective rate.
- Provincial rates, not only federal.
- Where savings are directed: RRSP, TFSA, non-registered, or corporate.

## A3: Retirement Projections

### Accumulation

- Current portfolio by account type.
- Annual contributions. RRSP at 18 percent of prior-year earned income to the
  annual limit, plus carry-forward room. TFSA at the annual limit plus unused
  room and prior withdrawals. Non-registered. Corporate retained earnings.
- Expected return by asset class from RBC CMAs, including the alternatives
  sleeve at its target weight. Do not benchmark to a 60/40.
- **Monte Carlo.** Probability of success across spending levels. Run it.

### Decumulation, the part that matters

- **RRSP to RRIF conversion.** Mandatory by December 31 of the year the client
  turns 71. Model the conversion year explicitly.
- **RRIF minimums.** Age-based factors on the January 1 balance. A younger
  spouse's age may be elected to reduce the factor.
- **CPP timing.** Start between 60 and 70. Early means a permanent reduction,
  deferral a permanent enhancement. Model 60, 65 and 70.
- **OAS timing and recovery tax.** Start between 65 and 70. The recovery tax
  claws back 15 percent of net income above the threshold, to full elimination
  at the upper bound. This is the single biggest planning lever in most
  Canadian retirements.
- **Withdrawal sequencing.** Model the order, do not assume it.
  - Drawing RRSP or RRIF early can reduce forced income later, lowering lifetime
    OAS clawback and the tax on the terminal return.
  - TFSA generally last. Tax-free growth, and it passes to a successor holder
    outside the estate.
  - Corporate money needs integration analysis: salary against dividend, CDA
    balance, passive income grinding the small business deduction.
- **Pension income splitting.** Up to 50 percent of eligible pension income
  with a spouse from 65. RRIF income qualifies; RRSP withdrawals do not. CPP
  sharing is separate and also available.
- **RRSP meltdown.** Where suitable, deliberate early RRSP drawdown, often
  paired with an investment loan or IFA, to shift income out of the high-rate
  terminal year. Model it and stage it for the accountant.

### Key output

- Projected portfolio at retirement by account type, not a single total. The
  tax character matters.
- Sustainable spending in after-tax dollars.
- Probability of success, target above 85 percent.
- Lifetime OAS retained against clawed back under each sequencing scenario.
- Estate value after the terminal-return tax.

## A4: Education Funding, RESP

- Beneficiary ages and target start.
- Current balance and CESG received to date. The grant is a 20 percent federal
  match on contributions, with annual and lifetime caps and carry-forward of one
  prior year's room. Confirm current figures.
- Provincial incentives where applicable.
- Contribution schedule that maximises grant rather than front-loading past it.
- Withdrawal mechanics. EAP, being grant plus growth, is taxable to the
  student. Return of contributions is tax-free. Sequence to use the student's
  low bracket.
- Over-contribution penalties. What happens if the child does not attend: AIP,
  RRSP transfer room, grant repayment.

## A5: Estate, Canadian Mechanics

**Canada has no estate tax.** The exposures are different:

- **Deemed disposition at death.** The entire portfolio is treated as sold at
  fair market value. Usually the largest single tax event in a client's life.
  Model it.
- **Spousal rollover.** Deferral to the surviving spouse or a qualifying spousal
  trust. The bill lands on the second death. Plan to that date.
- **Registered accounts.** RRSP and RRIF fall fully into income on the terminal
  return absent a qualifying rollover. Often the top marginal rate on the full
  balance.
- **Probate fees.** Provincial and variable. Ontario's estate administration tax
  is material above the first tier; Alberta's is capped and nominal. Structure
  accordingly: multiple wills, joint ownership with care, beneficiary
  designations, alter-ego or joint-partner trusts from age 65.
- **Corporate estates.** Post-mortem planning, being pipeline and loss
  carryback. CDA extraction. Double-tax risk on private company shares.
- **IFA, Insurance Financing Arrangements.** For the right UHNW client, the tool
  that funds the terminal tax bill without liquidating the portfolio. Treat it
  under estate and risk management, not as an investment product.
- **Charitable giving.** Donation of appreciated securities in kind eliminates
  the capital gain. Gifts by will and by designation.

## A6: Risk Management

- Life insurance needs: terminal tax liability, debt payoff, income replacement,
  estate equalisation among children.
- Corporate-owned against personally-owned policy, and the CDA credit on death.
- Disability and critical illness.
- Long-term care. Provincial coverage is partial. Model the shortfall.
- Umbrella liability.

## A7: Scenario Modeling

| Scenario | P(Success) | Estate After Tax | Lifetime OAS Retained | Notes |
|----------|-----------|------------------|-----------------------|-------|
| Base case | | | | |
| Retire 2 years early | | | | |
| 20% drawdown in year 1 | | | | |
| Spending +20% | | | | |
| CPP/OAS deferred to 70 | | | | |
| RRSP meltdown from 60 | | | | |
| Surviving spouse to 95 | | | | |
| LTC event, 4 years | | | | |

Sequence-of-returns risk gets its own scenario. A poor first five years of
decumulation does more damage than the same loss a decade later. Show it.

## A8: Recommendations

Prioritised, with owners. Take the current team roster from `firm-context`.

1. Contribution and savings changes: RRSP against TFSA against corporate.
2. Asset location across registered, non-registered and corporate accounts.
3. Decumulation sequence and CPP/OAS start ages.
4. Alternatives sleeve toward the 20 to 30 percent target where suitable and
   eligible.
5. Tax-loss harvesting on non-registered sleeves. The superficial loss rule
   governs: a loss is denied if identical property is bought 30 days before or
   after the sale by the taxpayer or an affiliated person, which includes a
   spouse, a controlled corporation, an RRSP or a TFSA.
6. Insurance gaps, including terminal tax funding.
7. Estate document and beneficiary review.
8. Items staged for the accountant.

## A9: Output

- Plan document, 15 to 25 pages. Client-facing layer plain, internal layer
  technical.
- Cash flow and decumulation projection in Excel.
- Retirement and estate-value charts.
- Scenario comparison table.
- Action checklist with owners and dates.

---

# Track B: Cross-border household

Use this when the gate returned Track B. **Start from Track A in full**, then
add only the blocks whose triggers fired. Name the trigger in the plan beside
each block so the reader knows why it is there.

A trigger that did not fire contributes nothing. Do not import a jurisdiction's
rules by analogy: U.S. rules do not describe the United Kingdom, and vice versa.

## B1: Trigger, a person is a U.S. person

Fires on U.S. citizenship, a green card, or meeting the substantial presence
test. Applies to that person only.

- **Filing.** A U.S. person files a U.S. return on worldwide income regardless
  of residence. The treaty and foreign tax credits relieve double taxation;
  they do not remove the filing obligation.
- **TFSA.** Not recognised by the IRS. Commonly a 3520 and 3520-A reporting
  problem and often the wrong account for this person entirely. Raise it before
  funding, not after.
- **RESP.** Same treatment. Raise it before funding.
- **PFIC.** Canadian mutual funds and ETFs are generally PFICs to a U.S.
  person, with punitive treatment and heavy reporting. Drives the product
  selection for that person's accounts, not just the reporting.
- **Reporting.** FBAR and Form 8938 on non-U.S. accounts.
- **U.S. retirement accounts.** Where the person holds an IRA, Roth or 401(k)
  while resident in Canada: treaty deferral election, withholding on
  distribution, and the Canadian reporting that follows.
- **Social Security.** Coordinate with CPP and OAS. The totalisation agreement
  and the treaty article govern. Do not model it as a straight add-on.
- **Estate.** A U.S. person has U.S. estate tax exposure on worldwide assets
  against the lifetime exemption, which is a different analysis from the
  situs-only exposure in B2.
- **Mixed household.** Where only one spouse is a U.S. person, joint ownership,
  spousal rollovers, gifting between spouses and successor-holder designations
  all need checking against both regimes. Flag it as its own item.

## B2: Trigger, U.S.-situs assets without U.S. personhood

Fires when a non-U.S. person holds U.S.-situs property: U.S. stocks, U.S. real
estate.

- U.S. estate tax can apply to a Canadian who is not a U.S. person. Treaty
  relief is prorated and is not automatic.
- Quantify the exposure and structure around it.
- Load nothing from B1. This person has no U.S. filing, FBAR, 3520 or PFIC
  exposure by reason of situs alone.

## B3: Trigger, non-U.S. foreign residency, citizenship or assets

Fires on residence, citizenship or situs assets in any country other than
Canada and the United States.

Do not reach for U.S. rules here. Establish, for the actual jurisdiction:

- Whether Canada has a tax treaty with it, and what the residency tie-breaker
  and the relevant articles say.
- Local income tax on the income types the client holds.
- Local inheritance, succession, gift or wealth tax, which several countries
  levy and Canada does not.
- Forced heirship or civil-law succession rules, which can override a Canadian
  will on local assets.
- Local recognition of Canadian registered accounts and trusts, which is often
  nil.
- Local reporting and filing obligations.
- Whether local counsel is required. Usually yes. Stage it.

## B4: Trigger, foreign property held by a Canadian resident

Fires on specified foreign property. Independent of citizenship.

- T1135 Foreign Income Verification Statement, where the cost of specified
  foreign property exceeds the CAD 100,000 threshold. Confirm the current
  threshold and the reporting tier.
- Currency: report the holding in CAD for the plan, and state the rate and date
  used. Keep the foreign-currency figure beside it only where the client
  transacts in that currency.

## B5: Trigger, a move in or out of Canada during the plan horizon

- **Departure tax.** Ceasing Canadian residence triggers a deemed disposition
  of most property. Model it against the departure year.
- Treaty residency tie-breakers for the year of the move.
- Which accounts survive the move and which should be unwound beforehand.
- For a snowbird, day counts in the destination country and whatever test it
  applies.
- Sequencing: several of these are cheaper to do before the move than after.

---

## Notes

- Plans are living documents. Review annually and after any major life event,
  and re-run Step 0 each time.
- Be conservative on returns. Overestimating gives false confidence, and the
  client remembers the number.
- In Canada the decumulation sequence is often worth more than the return
  assumption. Model it properly.
- Never blend income types into a single tax rate.
- A plan that only works in the base case is not a plan.
- Tax and legal conclusions are drafted for the accountant or counsel to
  confirm. Nothing here is a tax opinion.
- Compliance: CIRO suitability applies. Nothing here is advice until reviewed
  and signed off. Client-facing material goes through RBC DS compliance.
- Short sentences. Active voice. No em dashes. No emojis.
