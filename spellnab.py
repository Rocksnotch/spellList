import requests
import sys
from xml.dom import minidom
from bs4 import BeautifulSoup

schools = ["Conjuration", "Necromancy", "Evocation", "Abjuration", "Transmutation", "Divination", "Enchantment", "Illusion"]
spellType = ["Cantrip", "1st Level", "2nd Level", "3rd Level", "4th Level", "5th Level", "6th Level", "7th Level", "8th Level", "9th Level"]

indexSpell = 1
indexType = 0
spellTemp = 0
currentLen = 0

spellDetails = []

url = "http://dnd5e.wikidot.com/spells"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

root = minidom.Document()
xml = root.createElement('SpellList')
root.appendChild(xml)

for x in schools:
    schoolChild = root.createElement("School")
    schoolChild.setAttribute('name', x)
    xml.appendChild(schoolChild)

xml_str = root.toprettyxml(indent="\t")
save_path_file = "spellList.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
    
doc = minidom.parse("spellList.xml")

while (indexType < 10): #Goes thru Cantrip to 9th level
    wikiTab = "wiki-tab-0-" + str(indexType)
    wikiDiv = soup.find("div", id=wikiTab)
    tableRefs = wikiDiv.find_all("tr")
    currentLen = len(tableRefs)
    while (indexSpell < currentLen): #Goes thru all spells in current spell tab
        spellsInList = tableRefs[indexSpell].find_all("td")
        while (spellTemp < 6): #Goes thru all spell elements
            spellDetails.append(spellsInList[spellTemp].text)
            spellTemp += 1
        spellTemp = 0
        
        #Process the data here, stored in list 'spellDetails'
        
        dom = minidom.parse(r"spellList.xml")
        
        newSpell = dom.createElement("Spell")
        newSpell.setAttribute('name', spellDetails[0])
        
        match spellDetails[1]:
            case "Conjuration":
                schoolPick = dom.getElementsByTagName("School")[0]
            case "Necromancy":
                schoolPick = dom.getElementsByTagName("School")[1]
            case "Evocation":
                schoolPick = dom.getElementsByTagName("School")[2]
            case "Abjuration":
                schoolPick = dom.getElementsByTagName("School")[3]
            case "Transmutation":
                schoolPick = dom.getElementsByTagName("School")[4]
            case "Divination":
                schoolPick = dom.getElementsByTagName("School")[5]
            case "Enchantment":
                schoolPick = dom.getElementsByTagName("School")[6]
            case "Illusion":
                schoolPick = dom.getElementsByTagName("School")[7]
        
        schoolPick.appendChild(newSpell)
        
        spellLvl = dom.createElement("Level")
        lvlTxt = dom.createTextNode(spellType[indexType])
        spellLvl.appendChild(lvlTxt)
        newSpell.appendChild(spellLvl)
        
        spellCast = dom.createElement("CastTime")
        castTxt = dom.createTextNode(spellDetails[2])
        spellCast.appendChild(castTxt)
        newSpell.appendChild(spellCast)
        
        spellRange = dom.createElement("Range")
        rangeTxt = dom.createTextNode(spellDetails[3])
        spellRange.appendChild(rangeTxt)
        newSpell.appendChild(spellRange)
        
        spellDur = dom.createElement("Duration")
        durTxt = dom.createTextNode(spellDetails[4])
        spellDur.appendChild(durTxt)
        newSpell.appendChild(spellDur)
        
        spellComp = dom.createElement("Components")
        compTxt = dom.createTextNode(spellDetails[5])
        spellComp.appendChild(compTxt)
        newSpell.appendChild(spellComp)
        
        def pretty_print(dom):
            return '\n'.join([line for line in dom.toprettyxml(indent=' '*4).split('\n') if line.strip()])
        with open(save_path_file, "w") as f:
            f.write(pretty_print(dom))
        
        spellDetails.clear()
        indexSpell += 1
    indexSpell = 1
    indexType += 1