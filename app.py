import os

from flask import Flask, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")

        note = "PATIENT IDENTIFICATION: "
        note += name
        note += " is a "

        age = request.form.get("age")
        gender = request.form.get("gender")
        if gender == "male":
            nom = "He"
            gen = "His"
        elif gender == "female":
            nom = "She"
            gen = "Her"
        else:
            nom = "They"
            gen = "Their"
            gender += " individual"

        if gender == "male" or gender == "female":
            link = "is"
            linkp = "was"
            poss = "has"
        else:
            link = "are"
            linkp = "were"
            poss = "have"
        if age:
            note += age
            note += "-year-old "

        note += gender

        municipality = request.form.get("municipality")
        if municipality:
            note += " living in "
            note += municipality

        note += ". "

        employedornot = request.form.get("employedornot")
        incomesource = request.form.get("incomesource")

        if not employedornot and incomesource:
            note += gen
            note += " source of income is "
            note += incomesource
            note += ". "
        elif employedornot and not incomesource:
            note += nom
            note += " " + link + " "
            note += employedornot
            note += ". "
        elif employedornot and incomesource:
            if employedornot == "employed":
                note += nom
                note += " " + link + " employed as a "
                note += incomesource
                note += ". "
            else:
                note += nom
                note += " " + link + " unemployed and is financially supported by "
                note += incomesource
                note += ". "

        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")
        if starttime or endtime:
            if not starttime:
                starttime = "____"
            if not endtime:
                endtime = "____"
            note += nom
            note += " " + linkp + " seen from "
            note += starttime
            note += " to "
            note += endtime
            note += ". "

        note += "\n\n"

        reasonforreferral = request.form.get("reasonforreferral")
        if reasonforreferral:
            note += "REASON FOR REFERRAL: "
            note += reasonforreferral
            note += ".\n\n"

        note += "HISTORY OF PRESENT ILLNESS: "

        hpiflag = 0

        hpitext1 = request.form.get("hpitext1")
        if hpitext1:
            note += hpitext1
            note += "\n\n"
            hpiflag = 1

        dep = request.form.get("dep")
        depdes = request.form.get("depdes")
        depdur = request.form.get("depdur")

        paraflag = 0
        depmood = ""
        if dep == "low":
            depmood = "low"
        elif dep == "other" and depdes:
            depmood = depdes

        if depmood:
            paraflag = 1
            note += gen
            note += " mood has been "
            note += depmood

            if depdur:
                note += " for "
                note += depdur

            note += ". "

        anhedonia = request.form.get("anhedonia")
        if anhedonia == "present":
            paraflag = 1
            note += nom
            note += " " + poss + " experienced anhedonia. "
        elif anhedonia == "absent":
            paraflag = 1
            note += nom
            note += " " + poss + " not experienced anhedonia. "

        sleep = request.form.get("sleep")
        sleepdes = request.form.get("sleepdes")
        sleepdur = request.form.get("sleepdur")

        if sleep == "other":
            if sleepdes:
                sleep = sleepdes
            else:
                sleep = ""

        if sleep:
            paraflag = 1
            note += gen
            note += " sleep has been "
            note += sleep
            if sleepdur:
                note += ", with an average of "
                note += sleepdur
                note += " hours per night"
            note += ". "

        gw = request.form.get("gw")
        if gw:
            paraflag = 1
            if gw == "guilt":
                note += nom
                note += " " + poss + " had feelings of guilt. "
            elif gw == "worthlessness":
                note += nom
                note += " " + poss + " had feelings of worthlessness. "
            elif gw == "both":
                note += nom
                note += " " + poss + " had feelings of guilt and worthlessness. "
            else:
                note += nom
                note += " " + poss + " not had feelings of guilt or worthlessness. "

        energy = request.form.get("energy")
        energydes = request.form.get("energydes")
        if energy == "other":
            if energydes:
                energy = energydes
            else:
                energy = ""
        if energy:
            paraflag = 1
            note += gen
            note += " energy has been "
            note += sleep
            note += ". "

        concentration = request.form.get("concentration")
        concentrationdes = request.form.get("concentrationdes")
        if concentration == "other":
            if concentrationdes:
                concentration = concentrationdes
            else:
                concentration = ""
        if concentration:
            paraflag = 1
            note += gen
            note += " concentration has been "
            note += concentration
            note += ". "

        appetite = request.form.get("appetite")
        appetitedes = request.form.get("appetitedes")
        if appetite == "other":
            if appetitedes:
                appetite = appetitedes
            else:
                appetite = ""
        if appetite:
            paraflag = 1
            note += gen
            note += " appetite has been "
            note += appetite
            note += ". "

        psychomotor = request.form.get("psychomotor")
        psychomotordes = request.form.get("psychomotordes")
        if psychomotor == "other":
            if psychomotordes:
                psychomotor = psychomotordes
            else:
                psychomotor = ""
        if psychomotor:
            paraflag = 1
            note += gen
            note += " psychomotor activity has been "
            note += psychomotor
            note += ". "

        if paraflag == 1:
            note += "\n\n"
            paraflag = 0
            hpiflag = 1

        si = request.form.get("si")
        sides = request.form.get("sides")
        if si:
            paraflag = 1
            if si == "denied":
                note += nom
                note += " denied having suicidal ideation. "
            elif si == "passive":
                note += nom
                note += " " + poss + " had passive suicidal ideation, but no current plan or intent. "
            elif si == "active":
                note += nom
                note += " " + poss + " had active suicidal ideation"
                if sides:
                    note += ", with "
                    note += sides
                note += ". "

        sa = request.form.get("sa")
        sanum = request.form.get("sanum")
        sades = request.form.get("sades")

        if sa:
            paraflag = 1
            if sa == "absent":
                note += nom
                note += " " + poss + " no history of suicide attempts. "
            elif sa == "present":
                note += nom
                note += " " + poss + " a history of "
                if not sanum:
                    note += "suicide attempts. "
                elif sanum == "1":
                    note += "1 suicide attempt. "
                else:
                    note += sanum
                    note += " suicide attempts. "

        nssi = request.form.get("nssi")
        nssides = request.form.get("nssides")
        if nssi:
            paraflag = 1
            if nssi == "denied":
                note += nom
                note += " denied having thoughts of non-suicidal self-injury. "
            elif nssi == "passive":
                note += nom
                note += " " + poss + " had thoughts of non-suicidal self-injury, but has not acted on them. "
            elif nssi == "engaged":
                note += nom
                note += " " + poss + " engaged in non-suicidal self-injury"
                if nssides:
                    note += " by "
                    note += nssides
                note += ". "

        vi = request.form.get("vi")
        vides1 = request.form.get("vides1")
        vides2 = request.form.get("vides2")
        if vi:
            paraflag = 1
            if vi == "denied":
                note += nom
                note += " denied having violent ideation. "
            elif vi == "passive":
                note += nom
                note += " " + poss + " had passive violent ideation"
                if vides1:
                    note += ", with "
                    note += vides1
                note += ". "
            elif vi == "active":
                note += nom
                note += " " + poss + " had active suicidal ideation"
                if vides2:
                    note += ", with "
                    note += vides2
                note += ". "

        if paraflag == 1:
            note += "\n\n"
            paraflag = 0
            hpiflag = 1

        maniahistory = request.form.get("maniahistory")
        maniahistorydes = request.form.get("maniahistorydes")
        if maniahistory == "absent":
            paraflag = 1
            note += nom
            note += " " + poss + " no history of manic or hypomanic episodes. "
        elif maniahistory == "present":
            paraflag = 1
            note += nom
            note += " " + poss + " had a history of "
            if maniahistorydes:
                note += maniahistorydes
            else:
                note += "mania/hypomania"
            note += ". "

        mania = request.form.get("mania")
        maniades = request.form.get("maniades")
        maniadur = request.form.get("maniadur")
        if mania:
            if mania == "other":
                if maniades:
                    manmood = maniades
                else:
                    manmood = ""
            else:
                manmood = mania
        else:
            manmood = ""

        if manmood:
            paraflag = 1
            note += gen
            note += " mood has been "
            note += manmood
            if maniadur:
                note += " for "
                note += maniadur
            note += ". "

        distractibility = request.form.get("distractibility")
        if distractibility:
            paraflag = 1
            if distractibility == "absent":
                note += nom
                note += " " + poss + " not had distractibility. "
            elif distractibility == "present":
                note += nom
                note += " " + poss + " had distractibility. "

        impulsivity = request.form.get("impulsivity")
        if impulsivity:
            paraflag = 1
            if impulsivity == "absent":
                note += nom
                note += " " + poss + " not had impulsivity. "
            elif impulsivity == "present":
                note += nom
                note += " " + poss + " had impulsivity. "

        grandiosity = request.form.get("grandiosity")
        if grandiosity:
            paraflag = 1
            if grandiosity == "absent":
                note += nom
                note += " " + poss + " not had grandiosity. "
            elif grandiosity == "present":
                note += nom
                note += " " + poss + " had grandiosity. "

        racing = request.form.get("racing")
        if racing:
            paraflag = 1
            if racing == "absent":
                note += nom
                note += " " + poss + " not had racing thoughts. "
            elif racing == "present":
                note += nom
                note += " " + poss + " had racing thoughts. "

        activity = request.form.get("activity")
        if activity:
            paraflag = 1
            if activity == "goal-directed":
                note += nom
                note += " " + poss + " had increased goal-directed activity. "
            elif activity == "agitation":
                note += nom
                note += " " + poss + " had psychomotor agitation. "
            elif activity == "both":
                note += nom
                note += " " + poss + " had increased goal-directed activity and psychomotor agitation. "
            else:
                note += nom
                note += " " + poss + " not had increased goal-directed activity and psychomotor agitation. "

        needforsleep = request.form.get("needforsleep")
        needforsleepdes = request.form.get("needforsleepdes")
        needforsleepamount = request.form.get("needforsleepamount")
        if needforsleep == "other":
            if needforsleepdes:
                needforsleep = needforsleepdes
            else:
                needforsleep = ""
        if needforsleep:
            paraflag = 1
            note += gen
            note += " need for sleep has been "
            note += needforsleep
            if needforsleepamount:
                note += ", with "
                note += needforsleepamount
                note += " hours of sleep per night"
            note += ". "

        talk = request.form.get("talk")
        if talk:
            paraflag = 1
            if talk == "absent":
                note += nom
                note += " " + poss + " not had increased talkativeness. "
            elif talk == "present":
                note += nom
                note += " " + poss + " had increased talkativeness. "

        if paraflag == 1:
            note += "\n\n"
            paraflag = 0
            hpiflag = 1

        ga = request.form.get("ga")
        gadur = request.form.get("gadur")
        if ga:
            paraflag = 1
            if ga == "absent":
                note += nom
                note += " " + poss + " not had significant generalized anxiety. "
            elif ga == "present":
                note += nom
                note += " " + poss + " had significant generalized anxiety"
                if gadur:
                    note += " for "
                    note += gadur
                note += ". "

        restlessness = request.form.get("restlessness")
        if restlessness:
            paraflag = 1
            if restlessness == "absent":
                note += nom
                note += " " + poss + " not had restlessness. "
            elif restlessness == "present":
                note += nom
                note += " " + poss + " had restlessness. "

        fatiguability = request.form.get("fatiguability")
        if fatiguability:
            paraflag = 1
            if fatiguability == "absent":
                note += nom
                note += " " + poss + " not had easy fatiguability. "
            elif fatiguability == "present":
                note += nom
                note += " " + poss + " had easy fatiguability. "

        dc = request.form.get("dc")
        if dc:
            paraflag = 1
            if dc == "absent":
                note += nom
                note += " " + poss + " not had difficulty concentrating. "
            elif dc == "present":
                note += nom
                note += " " + poss + " had difficulty concentrating. "

        anxirr = request.form.get("anxirr")
        if anxirr:
            paraflag = 1
            if anxirr == "absent":
                note += nom
                note += " " + poss + " not had irritability. "
            elif anxirr == "present":
                note += nom
                note += " " + poss + " had irritability. "

        mt = request.form.get("mt")
        if mt:
            paraflag = 1
            if mt == "absent":
                note += nom
                note += " " + poss + " not had muscle tension. "
            elif mt == "present":
                note += nom
                note += " " + poss + " had muscle tension. "

        sd = request.form.get("sd")
        if sd:
            paraflag = 1
            if sd == "absent":
                note += nom
                note += " " + poss + " not had sleep disturbance. "
            elif sd == "present":
                note += nom
                note += " " + poss + " had sleep disturbance. "

        if paraflag == 1:
            note += "\n\n"
            paraflag = 0
            hpiflag = 1

        ah = request.form.get("ah")
        ahdes = request.form.get("ahdes")
        if ah:
            paraflag = 1
            if ah == "absent":
                note += nom
                note += " " + poss + " not had auditory hallucinations. "
            elif ah == "present":
                note += nom
                note += " " + poss + " had auditory hallucinations"
                if ahdes:
                    note += ", described as "
                    note += ahdes
                note += ". "

        vh = request.form.get("vh")
        vhdes = request.form.get("vhdes")
        if vh:
            paraflag = 1
            if vh == "absent":
                note += nom
                note += " " + poss + " not had visual hallucinations. "
            elif vh == "present":
                note += nom
                note += " " + poss + " had visual hallucinations"
                if vhdes:
                    note += ", described as "
                    note += vhdes
                note += ". "

        delusion = request.form.get("del")
        deldes = request.form.get("deldes")
        if delusion:
            paraflag = 1
            if delusion == "absent":
                note += nom
                note += " " + poss + " not had delusions. "
            elif delusion == "present":
                note += nom
                note += " " + poss + " had delusions"
                if deldes:
                    note += ", including delusions of "
                    note += deldes
                note += ". "
        delusionlist = []
        delscreenper = request.form.get("delscreenper")
        delscreenref = request.form.get("delscreenref")
        delscreeniwb = request.form.get("delscreeniwb")
        delscreenjea = request.form.get("delscreenjea")
        delscreengra = request.form.get("delscreengra")
        if delscreenper:
            delusionlist.append(delscreenper)
        if delscreenref:
            delusionlist.append(delscreenref)
        if delscreeniwb:
            delusionlist.append(delscreeniwb)
        if delscreenjea:
            delusionlist.append(delscreenjea)
        if delscreengra:
            delusionlist.append(delscreengra)
        if len(delusionlist) > 0:
            paraflag = 1
            note += nom
            note += " screened negative for delusions of "
            if len(delusionlist) == 1:
                note += delusionlist[0]
            elif len(delusionlist) == 2:
                note += delusionlist[0]
                note += " and "
                note += delusionlist[1]
            else:
                for i in range(len(delusionlist)-1):
                    note += delusionlist[i]
                    note += ", "
                note += "and "
                note += delusionlist[len(delusionlist)-1]
            note += ". "

        if paraflag == 1:
            note += "\n\n"
            paraflag = 0
            hpiflag = 1

        hpitext2 = request.form.get("hpitext2")
        if hpitext2:
            note += hpitext2
            note += "\n\n"
            hpiflag = 1

        if hpiflag == 0:
            note += "\n\n"

        pphtext = request.form.get("pphtext")
        if pphtext:
            note += "PAST PSYCHIATRIC HISTORY: "
            note += pphtext
            note += "\n\n"

        pmh = request.form.get("pmh")
        pmhlist = []
        for i in range(1, 6):
            if request.form.get(f"pmh{i}"):
                pmhlist.append(request.form.get(f"pmh{i}"))
        pmhtext = request.form.get("pmhtext")
        if pmh == "absent":
            note += "PAST MEDICAL HISTORY: None.\n\n"
        elif pmh == "present":
            if len(pmhlist) > 0 or pmhtext:
                note += "PAST MEDICAL HISTORY:\n"
                for i in range(len(pmhlist)):
                    note += f"{i+1}. "
                    note += pmhlist[i]
                    note += "\n"
                note += "\n"
                if pmhtext:
                    note += pmhtext
                    note += "\n\n"

        med = request.form.get("med")
        medlist = []
        for i in range(1, 6):
            if request.form.get(f"med{i}"):
                medlist.append(request.form.get(f"med{i}"))
        medtext = request.form.get("medtext")
        if med == "absent":
            note += "MEDICATIONS: None.\n\n"
        elif med == "present":
            if len(medlist) > 0 or medtext:
                note += "MEDICATIONS:\n"
                for i in range(len(medlist)):
                    note += f"{i+1}. "
                    note += medlist[i]
                    note += "\n"
                note += "\n"
                if medtext:
                    note += medtext
                    note += "\n\n"

        all = request.form.get("all")
        alldes = request.form.get("alldes")
        if all:
            if all == "absent":
                note += "ALLERGIES: None.\n\n"
            elif all == "present" and alldes:
                note += "ALLERGIES: " + alldes + ".\n\n"

        smokes = request.form.get("smokes")
        smokesdes = request.form.get("smokesdes")
        drinks = request.form.get("drinks")
        drinksdes = request.form.get("drinksdes")
        drugs = request.form.get("drugs")
        drugsdes = request.form.get("drugsdes")
        suhtext = request.form.get("suhtext")

        suh = 0
        if smokes == "absent" or (smokes == "present" and smokesdes):
            suh = 1
        if drinks == "absent" or (drinks == "present" and drinksdes):
            suh = 1
        if drugs == "absent" or (drugs == "present" and drugsdes):
            suh = 1
        if suhtext:
            suh = 1

        if suh == 1:
            note += "SUBSTANCE USE HISTORY: "
            if smokes == "absent":
                note += nom
                note += " denied smoking cigarettes. "
            elif smokes == "present" and smokesdes:
                note += nom
                if gender == "male" or gender == "female":
                    note += " smokes "
                else:
                    note += " smoke "
                note += smokesdes + ". "

            if drinks == "absent":
                note += nom
                note += " denied drinking alchohol. "
            elif drinks == "present" and drinksdes:
                note += nom
                if gender == "male" or gender == "female":
                    note += " drinks "
                else:
                    note += " drink "
                note += drinksdes + ". "

            if drugs == "absent":
                note += nom
                note += " denied use of recreational drugs. "
            elif drugs == "present" and drugsdes:
                note += nom
                if gender == "male" or gender == "female":
                    note += " uses "
                else:
                    note += " use "
                note += drugsdes + ". "
            note += "\n\n"

            if suhtext:
                note += suhtext
                note += "\n\n"

        fph = request.form.get("fph")
        fphdes = request.form.get("fphdes")
        if fph:
            if fph == "absent":
                note += "FAMILY PSYCHIATRIC HISTORY: None.\n\n"
            elif fph == "present" and fphdes:
                note += "FAMILY PSYCHIATRIC HISTORY: " + fphdes + "\n\n"

        shtext = request.form.get("shtext")
        if shtext:
            note += "SOCIAL HISTORY: "
            note += shtext
            note += "\n\n"

        note += "MENTAL STATUS EXAMINATION: "

        msea = request.form.get("msea")
        mseades = request.form.get("mseades")
        if msea:
            if msea == "normal":
                note += nom
                note += " " + linkp + " appropriately dressed and groomed. "
            elif msea == "other" and mseades:
                note += mseades + " "

        mseb = request.form.get("mseb")
        msebdes = request.form.get("msebdes")
        if mseb:
            if mseb == "normal":
                note += "There were no abnormal movements seen. "
            elif mseb == "other" and msebdes:
                note += msebdes + " "

        msec = request.form.get("msec")
        msecdes = request.form.get("msecdes")
        if msec:
            if msec == "cooperative":
                note += nom
                note += " " + linkp + " cooperative. "
            elif msec == "guarded":
                note += nom
                note += " " + linkp + " guarded. "
            elif msec == "other" and msecdes:
                note += msecdes + " "

        msem = request.form.get("msem")
        if msem:
            note += gen
            note += " mood was "
            note += msem
            note += ". "

        mseaq = request.form.get("mseaq")
        mseaqdes = request.form.get("mseaqdes")
        if mseaq == "other":
            if mseaqdes:
                mseaq = mseaqdes
            else:
                mseaq = ""
        msear = request.form.get("msear")
        mseardes = request.form.get("mseardes")
        if msear == "other":
            if mseardes:
                msear = mseardes
            else:
                msear = ""

        if mseaq and not msear:
            note += nom
            note += " affect was "
            note += mseaq
            note += ". "
        if not mseaq and msear:
            note += nom
            note += " affect was "
            note += msear
            note += ". "
        if mseaq and msear:
            note += nom
            note += " affect was "
            note += mseaq
            note += " and "
            note += msear
            note += ". "

        mses = request.form.get("mses")
        msesdes = request.form.get("msesdes")
        if mses:
            if mses == "normal":
                note += gen
                note += " speech was normal in rate, rhythm, and volume. "
            elif mses == "other" and msesdes:
                note += msesdes + " "

        msetf = request.form.get("msetf")
        msetfdes = request.form.get("msetfdes")
        if msetf:
            if msetf == "normal":
                note += gen
                note += " thought form was linear and goal directed. "
            elif msetf == "other" and msetfdes:
                note += msetfdes + " "

        msetc = request.form.get("msetc")
        msetcdes = request.form.get("msetcdes")
        if msetc:
            if msetc == "normal":
                note += gen
                note += " thought content was normal, with no delusional beliefs. "
            elif msetc == "other" and msetcdes:
                note += gen
                note += " thought content included "
                note += msetcdes + ". "

        msep = request.form.get("msep")
        msepdes = request.form.get("msepdes")
        if msep:
            if msep == "normal":
                note += "There was no evidence of perceptual abnormalities. "
            elif msep == "other" and msepdes:
                note += msepdes + " "

        msesi = request.form.get("msesi")
        msesides = request.form.get("msesides")
        if msesi:
            if msesi == "denied":
                note += nom
                note += " denied having suicidal ideation. "
            elif msesi == "passive":
                note += nom
                note += " " + poss + " had passive suicidal ideation, but no current plan or intent. "
            elif msesi == "active":
                note += nom
                note += " " + poss + " had active suicidal ideation"
                if msesides:
                    note += ", with "
                    note += msesides
                note += ". "

        msevi = request.form.get("msevi")
        msevides1 = request.form.get("msevides1")
        msevides2 = request.form.get("msevides2")
        if msevi:
            paraflag = 1
            if msevi == "denied":
                note += nom
                note += " denied having violent ideation. "
            elif msevi == "passive":
                note += nom
                note += " " + poss + " had passive violent ideation"
                if msevides1:
                    note += ", with "
                    note += msevides1
                note += ". "
            elif msevi == "active":
                note += nom
                note += " " + poss + " had active suicidal ideation"
                if msevides2:
                    note += ", with "
                    note += msevides2
                note += ". "

        msecog = request.form.get("msecog")
        msecogdes = request.form.get("msecogdes")
        if msecog:
            if msecog == "normal":
                note += "Cognition was grossly intact. "
            elif msecog == "other" and msecogdes:
                note += msecogdes + " "

        msei = request.form.get("msei")
        mseides = request.form.get("mseides")
        if msei == "other":
            if mseides:
                msei = mseides
            else:
                msei = ""
        if msei:
            note += gen
            note += " insight was "
            note += msei
            note += ". "

        msej = request.form.get("msej")
        msejdes = request.form.get("msejdes")
        if msej == "other":
            if msejdes:
                msej = msejdes
            else:
                msej = ""
        if msej:
            note += gen
            note += " judgment was "
            note += msej
            note += ". "

        note += "\n\n"

        dxlist = []
        for i in range(1, 6):
            if request.form.get(f"dx{i}"):
                dxlist.append(request.form.get(f"dx{i}"))
        if len(dxlist) > 0:
            if len(dxlist) == 1:
                note += "DIAGNOSIS: " + dxlist[0] + "\n\n"
            else:
                note += "DIAGNOSES:\n"
                for i in range(len(dxlist)):
                    note += f"{i+1}. "
                    note += dxlist[i]
                    note += "\n"
                note += "\n"

        assesstext = request.form.get("assesstext")
        if assesstext:
            note += "ASSESSMENT: "
            note += assesstext
            note += "\n\n"


        planlist = []
        for i in range(1, 6):
            if request.form.get(f"plan{i}"):
                planlist.append(request.form.get(f"plan{i}"))
        plantext = request.form.get("plantext")
        if len(planlist) > 0 or plantext:
            note += "PLAN:\n"
            for i in range(len(planlist)):
                note += f"{i+1}. "
                note += planlist[i]
                note += "\n"
            note += "\n"
            if plantext:
                note += plantext

        note = note.split("\n")
        return render_template("note.html", note=note)
    else:
        return render_template("index.html")
