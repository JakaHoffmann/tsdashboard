import requests
import random

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import Counter
from datetime import datetime
from sqlalchemy import and_
from tsdashboard import db
from tsdashboard.models import ApiModel, QradarDomainModel, UserModel, OffenseModel, QradarCategoryLowModel, QradarUserModel, QradarCategoryHighModel

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Siem(object):
    def povezavaZdb(self, neki):
        if neki is "ALL":
            api_podjetja = ApiModel.query.all()
        else:
            api_podjetja = ApiModel.query.filter(ApiModel.ime.ilike(neki + "%")).all()

        if not api_podjetja:
            return None

        return api_podjetja

    def povezavaZapi(self, url, version=None, num_of_items=None):
        if self._srch is not None:
            odgovor = {}

            for x in self._srch:
                glava = {'SEC': x.api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': "13.1", 'Range': 'items=0-49'}
                try:
                    with self._connection as s:
                        r = s.get(x.url + url, headers=glava, verify=False)
                        r.raise_for_status()
                    odgovor[x.ime] = r.json()
                except requests.exceptions.HTTPError as err:
                    print("ERROR ERROR ERROR: {}".format(err))
                    if r.status_code == requests.codes.forbidden:
                        print("403 403 403 403 403 403 403 403 403")
                except requests.exceptions.ConnectionError as errc:
                    print ("ERROR CONNECTING, ker so testne 'povezave': {}".format(errc))

            return odgovor
        return None

    def getDataFromDB(self, whatIneed, whereToLook) -> dict:
        podatki = {}
        if whereToLook is "ApiModel":
            data = ApiModel.query.all()
        elif whereToLook is "UserModel": pass
        elif whereToLook is "UserRoleModel": pass
        elif whereToLook is "QradarDomainModel": pass
        else: "You shall not pass"

        for i in data:
            for j in whatIneed:
                print(j)

        return data[0].url

    def setDataToDB(self, whereToPut): pass

    def povezavaZapi2(self, url, api_key, version=None, num_of_items=None, filter=None):
        _connection = requests.Session()
        odgovor = 0
        if version is not None and num_of_items is not None and filter is None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '{}'.format(version), 'Range': 'items=0-{}'.format(num_of_items)}
        elif version is None and num_of_items is not None and filter is None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '12.0', 'Range': 'items=0-{}'.format(num_of_items)}
        elif version is not None and num_of_items is None and filter is None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '{}'.format(version), 'Range': 'items=0-10'}
        else:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '12.0'}

        try:
            with _connection as s:
                r = s.get(url, headers=glava, verify=False)
                r.raise_for_status()
            odgovor = r.json()
        except requests.exceptions.HTTPError as err:
            print("ERROR HTTP: {}".format(err))
            if r.status_code == requests.codes.forbidden:
                print("403 403 403")
        except requests.exceptions.ConnectionError as errc:
            print ("ERROR CONNECTING': {}".format(errc))

        return odgovor


class Qradar(Siem):
    def __init__(self, kdo=None):
        if kdo is None:
            pass
        else:
            self._kdo = kdo
            self._srch = super().povezavaZdb(self._kdo)
            self._connection = requests.Session()

    def getOffense(self, apiID, offenseID): #pass
        url2 = "siem/offenses/" + str(offenseID)
        tmp = ApiModel.query.filter_by(id=apiID).first()
        data = super().povezavaZapi2(tmp.url + url2, tmp.api_key)

        return data

    def getOffenses(self):
        siem_podatki = {}
        url2 = "siem/offenses?filter=status%3Dopen&sort=-id"
        api_podatki = ApiModel.query.filter_by(izbor="qradar").all()
        for i in api_podatki:
            siem_podatki[i.ime] = super().povezavaZapi2(i.url + url2, i.api_key, num_of_items=9)
        return siem_podatki

    def getCategory(self, categoryID, tip): pass

    def getVulnerabilities(self): pass

    def getLegenda(self):
        podatki = {}
        data = ApiModel.query.all()
        for i in data:
            podatki[i.id] = i.ime
        return podatki

    def getDomains(self):
        podatki = {}
        data = QradarDomainModel.query.all()
        for row in data:
            tmp = {}
            tmp["domain_id"] = row.domain_id
            tmp["domain_name"] = row.domain_name
            tmp["ApiVnasalec"] = row.api_vnasalec.ime
            podatki[row.id] = tmp

        return podatki

    def domainsToDB(self):
        domain_url2 = "config/domain_management/domains"
        odgovor = super().povezavaZapi(domain_url2)
        if odgovor is not None:
            for y in odgovor:
                api_domene = ApiModel.query.filter_by(ime=y).first()
                for x in odgovor[y]:
                    obstaja_domena = QradarDomainModel.query.filter(and_(QradarDomainModel.api_model_id == api_domene.id, QradarDomainModel.domain_name == x["name"])).first()
                    if obstaja_domena is None:
                        domain = QradarDomainModel(domain_id=x["id"], domain_name=x["name"], description=x["description"])
                        api_domene.domains.append(domain)
                        db.session.add(api_domene)
                        db.session.add(domain)
                        db.session.commit()

            return True
        return False

    def getUserAdmin(self): pass
        # url2 = "config/access/users"
        # data = ApiModel.query.all()
        # for i in data:
        #     podatki = super().povezavaZapi2(i.url + url2, i.api_key, num_of_items=99)
        #     for j in podatki:
        #         ldapusername = UserModel.query.filter(UserModel.mail.ilike(j["email"] + "%")).first()
        #         if ldapusername:
        #             ldapusername.ldapuser = j["username"]
        #             db.session.commit()
        # return user


class QradarInterface(object): # klic v class QradarConfig()
    pass

    # def getOffense(self): pass
    # def getUsers(self): pass
    # def getVulnerabilities(self): pass
    # def getAsset(self): pass
    # def getClasification(self): pass
    # def getAnalytics(self): pass

class QradarStat(Siem):
    def __init__(self, what, num_of_items):
        self.what = what
        self.num_of_items = num_of_items

    def userData(self):
        user_podatki = {}
        user_data = self.getData()
        for key in user_data:
            user_podatki[key] = []
            for i in user_data[key]:
                if i["assigned_to"] is None:
                    user_podatki[key].append("None")
                else:
                    user_podatki[key].append(i["assigned_to"])
            tmp = Counter(user_podatki[key])
            
            user_podatki[key] = dict(zip(tmp.keys(),tmp.values()))
        return user_podatki

    def catData(self):
        cat_podatki = {}
        cat_data = self.getData()
        for key in cat_data:
            cat_podatki[key] = []
            
            print(cat_data[key])

            for i in cat_data[key]:
                cat_podatki[key].append(i["categories"])
            tmpList = [item for sublist in cat_podatki[key] for item in sublist]
            cat_podatki[key] = Counter(tmpList)
        return cat_podatki

    def getData(self):
        podatki = {}
        url2 = "siem/offenses?filter=status%3Dopen&sort=-id"
        api_podatki = ApiModel.query.filter_by(izbor="qradar").all()
        for i in api_podatki:
            podatki[i.ime] = super().povezavaZapi2(i.url + url2, i.api_key, num_of_items=self.num_of_items)
        return podatki
        

class Config(object):
    def __init__(self, izbor, key, url, access):
        self.izbor = izbor
        self.key = key
        self.url = url
        self.access = access

    def povezavaZapi(self, api_key, url, version=None, num_of_items=None, filter=None):
        _connection = requests.Session()
        odgovor = 0
        if version is not None and num_of_items is not None and filter is not None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '{}'.format(version), 'Range': 'items=0-{}'.format(num_of_items)}
        elif num_of_items is not None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '12.0', 'Range': 'items=0-{}'.format(num_of_items)}
        elif version is not None:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '{}'.format(version), 'Range': 'items=0-10'}
        else:
            glava = {'SEC': api_key, 'Content-Type':'Application/Json', 'Accept':'Application/Json', 'Version': '12.0', 'Range': 'items=0-10'}

        try:
            with _connection as s:
                tmp = s.get(url, headers=glava, verify=False)
                tmp.raise_for_status()
            odgovor = tmp.json()
        except requests.exceptions.HTTPError as err:
            print("ERROR HTTP: {}".format(err))
            if err.status_code == requests.codes.forbidden:
                print("403 403 403")
        except requests.exceptions.ConnectionError as errc:
            print ("ERROR CONNECTING': {}".format(errc))

        return odgovor


class QradarConfig(Config):
    def __init__(self, ime, key, url, access):
        self.ime = ime
        self.key = key
        self.url = url
        self.access = access
        self.id_last_offense = 0

    def setDomains(self):
        if self.access is True:
            domain_url2 = "config/domain_management/domains"
            odgovor = super().povezavaZapi(self.key, self.url + domain_url2)
            if odgovor is not None:
                api_domena = ApiModel.query.filter_by(ime=self.ime).first()
                for y in odgovor:
                    domain = QradarDomainModel(\
                            domain_id=y["id"],\
                            domain_name=y["name"],\
                            description=y["description"],\
                            barva="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])\
                            )
                    api_domena.domains.append(domain)
                    db.session.add(api_domena)
                    db.session.add(domain)
                    db.session.commit()
            else:
                return "ni domen ???"
        else:
            return "No Access for domain information"

    def setHighCategory(self):
        cat_url2 = "data_classification/high_level_categories"
        odgovor = super().povezavaZapi(self.key, self.url + offense_url2, num_of_items=100)
        if odgovor is not None:
            for i in odgovor:
                new_high_cat = QradarCategoryHighModel(\
                    id = i["id"],\
                    name = i["name"],\
                    description = i["description"],\
                    ime = self.ime\
                    )
                db.session.add(new_high_cat)
                db.session.commit()

    def setOffenses(self):
        offense_url2 = "siem/offenses?filter=status%3Dopen&sort=-id"
        odgovor = super().povezavaZapi(self.key, self.url + offense_url2, num_of_items=10)
        self.id_last_offense = odgovor[0]["id"]
        if odgovor is not None:
            for i in odgovor:
                new_offense = OffenseModel(\
                        offense_id=i["id"],\
                        start_time=i["start_time"] if i["start_time"] is not None else 0,\
                        close_time=i["close_time"] if i["close_time"] is not None else 0,\
                        credibility=i["credibility"],\
                        relevance=i["relevance"],\
                        severity=i["severity"],\
                        magnitude=i["magnitude"],\
                        status=i["status"],\
                        event_count=i["event_count"],\
                        flow_count=i["flow_count"],\
                        offense_type=i["offense_type"],\
                        offense_source=i["offense_source"],\
                        source_network=i["source_network"]\
                        )

                # CATEGORY POVEZAVA
                if i["category_count"] > 1:
                    for j in i["categories"]:
                        low_cat = self.getCategoryData(j)
                        new_offense.categories.append(low_cat)
                else:
                    low_cat = self.getCategoryData(i["categories"])
                    new_offense.categories.append(low_cat)

                # API POVEZAVA
                od_api_id = ApiModel.query.filter_by(ime=self.ime).first()
                new_offense.od_api_id.append(od_api_id)

                #DOMAIN POVEZAVA
                od_qradardomene_id = QradarDomainModel.query.filter(QradarDomainModel.api_model_id == od_api_id.id, QradarDomainModel.domain_id == i["domain_id"]).first()
                if od_qradardomene_id is not None:
                    new_offense.od_qradardomene_id.append(od_qradardomene_id)

                # USERNAME POVEZAVA
                username_in_db = QradarUserModel.query.filter_by(username=i["assigned_to"]).first()
                if username_in_db is None:
                    assigned_to = QradarUserModel(username=i["assigned_to"])
                    new_offense.assigned_to.append(assigned_to)
                else:
                    new_offense.assigned_to.append(username_in_db)

                db.session.add(new_offense)
                db.session.commit()
        else:
            return "Nobenih offensov ???"

    def getCategoryData(self, name):
        cat_url2 = "data_classification/low_level_categories"
        if isinstance(name, list):
            tmp = "".join(name)
            cat_url3 = "?filter=name%3D%22" + tmp + "%22"
        else:
            cat_url3 = "?filter=name%3D%22" + str(name) + "%22"
        odgovor = super().povezavaZapi(self.key, self.url + cat_url2 + cat_url3, num_of_items=3)
        ce_obstaja = QradarCategoryLowModel.query.filter_by(cat_id=odgovor[0]["id"]).first()
        if odgovor is not None and ce_obstaja is None:
            for i in odgovor:
                self.fillCategoryData(i["high_level_category_id"])
                high_cat_obj = QradarCategoryHighModel.query.filter_by(cat_id=str(i["high_level_category_id"])).first()
                new_low_cat = QradarCategoryLowModel(\
                    cat_id = i["id"],\
                    name = i["name"],\
                    description = i["description"],\
                    severity = i["severity"],\
                    high_level_category_id = i["high_level_category_id"],\
                    high_cat = i["high_level_category_id"]\
                    )
                
                high_cat_obj.low_cat.append(new_low_cat)
                return new_low_cat
        else: 
            return ce_obstaja

    def fillCategoryData(self, high_cat_id):
        high_cat_url2 = "data_classification/high_level_categories"
        high_cat_url3 = "?filter=id%3D" + str(high_cat_id)

        odgovor = super().povezavaZapi(self.key, self.url + high_cat_url2 + high_cat_url3, num_of_items=3)
        ce_obstaja = QradarCategoryHighModel.query.filter_by(cat_id=high_cat_id).first()
        if odgovor is not None and ce_obstaja is None:
            for i in odgovor:
                new_high_cat = QradarCategoryHighModel(\
                    cat_id = i["id"],\
                    name = i["name"],\
                    description = i["description"]\
                    )
                db.session.add(new_high_cat)
                db.session.commit()
        else:
            return "Ni kategorije ???"

    def checkIfExist(self, baza, vrednost): pass
    
    def checkIfNew(self):
        print(self.id_last_offense)
        offense_url2 = "siem/offenses?filter=status%3Dopen&sort=-id"
        odgovor = super().povezavaZapi(self.key, self.url + offense_url2, num_of_items=1)
        if odgovor is not None:
            return odgovor
        else:
            return "Nobenih novih offensov ???"