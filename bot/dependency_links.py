"""
Ссылки на ресурсы групп поддержки по зависимостям для разных городов.
"""

# Маппинг внутренних ключей на названия из файла
DEPENDENCY_MAPPING = {
    'alcohol': 'Алкогольная',
    'drugs': 'Наркотическая',
    'gaming': 'Игровая зависимость (Лудомания)',
    'food': 'Пищевая зависимость (РПП)',
    'internet': 'Интернет-зависимость',
    'nicotine': 'Никотиновая зависимость',
    'codependency': 'Созависимость',
    'vad': 'ВДА (взрослые дети алкоголиков)',
    'love': 'Любовная зависимость',
    'workaholism': 'Трудоголизм',
    'vr': 'ВР (Взрослый ребенок)'
}

# Структура: {город: {зависимость: ссылка}}
DEPENDENCY_LINKS = {
    'moscow': {
        'alcohol': 'https://ruscatalog.org/moskva/5849009-anonimnye-alkogoliki-gruppa-moskovskie-nachinajushhie/?utm_source=chatgpt.com',
        'drugs': 'https://na-russia.org/moskva',
        'gaming': 'https://gamblersanonymous.ru',
        'food': 'https://oamos.ru/?ysclid=mh7crwk6sv222890748',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://mcmk.su/gruppy-dlya-sozavisimyh?utm_source=chatgpt.com',
        'vad': 'https://vdamoscow.ru',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://narko-info.ru/directory-organization/gruppa-anonimnyh-trudogolikov-moskva/?utm_source=chatgpt.com',
        'vr': None
    },
    'spb': {
        'alcohol': 'https://aa-ssnp.com/?utm_source=chatgpt.com',
        'drugs': 'https://na-neva.ru/gruppy-an/?utm_source=chatgpt.com',
        'gaming': 'https://anocbsl.ru/?utm_source=chatgpt.com',
        'food': 'https://переедающие.рф/groups/live/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://coda-spb.ru/?ysclid=mh7dfq9vos798020095',
        'vad': 'https://sig-aca.orgs.biz/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'voronezh': {
        'alcohol': 'https://aavrn.ru/groups/',
        'drugs': 'https://na-russia.org/voronezh',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/live/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://voronezh.nan-rc.ru/gruppy-dlya-sozavisimyh/?utm_source=chatgpt.com',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'krasnodar': {
        'alcohol': 'https://aakrasnodar.ru/meetings.html',
        'drugs': 'https://na-krd.ru/meeting-schedule',
        'gaming': 'https://gamblersanonymous.ru/spisok-gorodov?ysclid=mhsuu1p3ox308197089',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://aakrasnodar.ru/vda.html',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'kazan': {
        'alcohol': 'https://aakazan.ru/groups/?ysclid=mh7f5mj6kp103034742',
        'drugs': 'https://na-kzn.ru/shtab.html?utm_source=chatgpt.com',
        'gaming': 'https://аи-поволжье.рф/raspisanie-sobranij?ysclid=mh7f3wb6dt31967012',
        'food': 'https://переедающие.рф/groups/live/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'samara': {
        'alcohol': 'https://www.aasamara.ru/schedule',
        'drugs': 'https://na-samara.com/?ysclid=mh7fvh03p8916718395',
        'gaming': 'https://аи-поволжье.рф/raspisanie-sobranij?ysclid=mh7f3wb6dt31967012',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'izhevsk': {
        'alcohol': 'https://aaudmurtiya.ru/?ysclid=mh7g9olatw532649330',
        'drugs': 'https://na-volga.ru/sobraniya-anonimnie-narkomani/anonimnyie-narkomanyi-v-izhevske/?ysclid=mh7gajo0w2523057079',
        'gaming': 'https://аи-поволжье.рф/raspisanie-sobranij?ysclid=mh7f3wb6dt31967012',
        'food': 'https://переедающие.рф/groups/live/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://vdaudmurtiya.tilda.ws',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'ekaterinburg': {
        'alcohol': 'https://aa-ekb.ru/groups?ysclid=mh7gbryirk640637135',
        'drugs': 'https://na-ekb.ru/meetings',
        'gaming': 'https://аи-поволжье.рф/raspisanie-sobranij?ysclid=mh7f3wb6dt31967012',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://alanon-ekb.ru/?ysclid=mh7gi4awjy176256578',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'chelyabinsk': {
        'alcohol': 'https://aachel.ru/raspisanie-sobranij-anonimnyh-alkogolikov-chelyabinsk-kopeisk/',
        'drugs': 'https://na-chel.ru/meetings/',
        'gaming': 'https://аи-поволжье.рф/raspisanie-sobranij?ysclid=mh7f3wb6dt31967012',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meeting/74-01?ysclid=mh7grj4hld141149368',
        'vad': 'https://vk.com/vda74?ysclid=mh7gsd76i2452656679',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'omsk': {
        'alcohol': 'https://aaomsk.ru/group-aa-optimist/',
        'drugs': 'https://an-sibiri.ru/omsk/?ysclid=mh7gvy8yu0975515782',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/live/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://al-anon-omsk.ru',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'barnaul': {
        'alcohol': 'https://www.aa-altai.ru/?ysclid=mh7hbdqq2o903823051',
        'drugs': 'https://an-sibiri.ru/barnaul/?ysclid=mh7hchvl4h748299577',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://vk.com/club162106399?ysclid=mh7hfqu1yw346789389',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'novosibirsk': {
        'alcohol': 'https://aansk.ru/?ysclid=mh7x90vjnd364483657',
        'drugs': 'https://na-nsk.ru/meetings/?ysclid=mh7xakrbch334582288',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'krasnoyarsk': {
        'alcohol': 'https://aa-enisey.ru/raspisanie-zhivyh-grupp/',
        'drugs': 'https://an-sibiri.ru/krasnoyarsk/?ysclid=mh7xk0eiqf496499740',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'irkutsk': {
        'alcohol': 'https://aa-irk.ru/?ysclid=mh7xrdh2c2367518758',
        'drugs': 'https://an-sibiri.ru/irkutsk/?ysclid=mh7xsjxd93753634883',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'ulan_ude': {
        'alcohol': 'https://aa-irk.ru/?ysclid=mh7xrdh2c2367518758',
        'drugs': 'https://na-russia.org/ulan-ude',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/meetings',
        'vad': 'https://adultchildren.ru/groups/online_list/',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'yakutsk': {
        'alcohol': 'https://aayakutia.aarussia.ru',
        'drugs': 'https://dv-na.ru/schedule/якутск/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'blagoveshchensk': {
        'alcohol': 'https://aablag.orgs.biz',
        'drugs': 'https://dv-na.ru/schedule/благовещенск/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://www.detki-v-setke.ru/index.php?showtopic=618',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'vladivostok': {
        'alcohol': 'https://aa25.ru',
        'drugs': 'https://dv-na.ru/schedule/владивосток/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'khabarovsk': {
        'alcohol': 'https://khv.aarussia.ru',
        'drugs': 'https://dv-na.ru/schedule/хабаровск/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://al-anon.org.ru/najti-sobranie/?_sft_sobranie=habarovsk',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'magadan': {
        'alcohol': 'https://aa-russia.com/doku.php/магаданская_область',
        'drugs': 'https://dv-na.ru/schedule/магадан/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://www.detki-v-setke.ru/index.php?showtopic=618',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'yuzhno_sakhalinsk': {
        'alcohol': 'https://sakh.aarussia.ru',
        'drugs': 'https://dv-na.ru/schedule/южно-сахалинск/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'petropavlovsk': {
        'alcohol': 'https://aa-russia.com/doku.php/камчатский_край',
        'drugs': 'https://dv-na.ru/schedule/петропаловск-камчатский/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://adultchildren.ru/groups/offline_list/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'anadyr': {
        'alcohol': 'https://aarus.ru/groups-aa-russia/133-groups-aa-russia/chukotka/344-anadyr',
        'drugs': 'https://dv-na.ru/online/',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://www.codarus.org/online',
        'vad': 'https://www.detki-v-setke.ru/index.php?showtopic=618',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    },
    'kaliningrad': {
        'alcohol': 'https://aarus.ru/groups-aa-russia/68-groups-aa-russia/kaliningradskaya/161-kaliningrad?utm_source=chatgpt.com',
        'drugs': 'https://vk.com/na_russia_official',
        'gaming': 'https://gamblersanonymous.ru/?ysclid=mh7hsvb958468190218',
        'food': 'https://переедающие.рф/groups/online/',
        'internet': 'https://internetaddictsanonymous.org/ru/local-internet-addiction-meetings/россия-москва/',
        'nicotine': 'https://ak-moscow.ru',
        'codependency': 'https://al-anon.org.ru/najti-sobranie/?_sft_sobranie=kaliningrad',
        'vad': 'https://vda--kaliningrad.orgs.biz/?utm_source=chatgpt.com',
        'love': 'https://laarus.ru/?ysclid=mhsuc6q433453047294',
        'workaholism': 'https://workaholics-anonymous.ru/raspisanie-sobranij/',
        'vr': None
    }
}


def get_dependency_link(city: str, dependency: str) -> str:
    """
    Получить ссылку на ресурс для конкретной зависимости и города.
    
    Args:
        city: Ключ города (например 'moscow', 'spb')
        dependency: Ключ зависимости (например 'alcohol', 'drugs')
        
    Returns:
        Ссылка на ресурс или None если не найдено
    """
    city_links = DEPENDENCY_LINKS.get(city, {})
    return city_links.get(dependency)
