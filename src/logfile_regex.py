_logLanguageRegex = {
    "english": {
        "character": "(?<=Listener: ).*",
        "sessionTime": "(?<=Session Started: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?P<default_ship>.*)\)<|<)/b.*> \-(?: (?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>to<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>from<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> remote armor repaired to <",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> remote hull repaired to <",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*> remote shield boosted to <",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> remote armor repaired by <",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> remote hull repaired by <",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*> remote shield boosted by <",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*> remote capacitor transmitted to <",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*> energy neutralized <",
        "nosRecieved": "\(combat\) <.*?><b>\+([0-9]+).*> energy drained from <",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*> remote capacitor transmitted by <",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>([0-9]+).*> energy neutralized <",
        "nosTaken": "\(combat\) <.*?><b>\-([0-9]+).*> energy drained to <",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*> units of <.*?><.*?>(.+?)<",
        "locklost": "\(combat\) .*target locks broken.*",
    },
    "russian": {
        "character": "(?<=Слушатель: ).*",
        "sessionTime": "(?<=Сеанс начат: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?:<localized .*?>)?(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?:<localized .*?>)?(?P<default_ship>.*)\)<|<)/b.*> \-(?: (?:<localized .*?>)?(?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>на<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>из<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности брони отремонтировано <",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности корпуса отремонтировано <",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности щитов накачано <",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности брони получено дистанционным ремонтом от <",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности корпуса получено дистанционным ремонтом от <",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса прочности щитов получено накачкой от <",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса энергии накопителя отправлено в <",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*> энергии нейтрализовано <",
        "nosRecieved": "\(combat\) <.*?><b>\+([0-9]+).*> энергии извлечено из <",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*> единиц запаса энергии накопителя получено от <",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>([0-9]+).*> энергии нейтрализовано <",
        "nosTaken": "\(combat\) <.*?><b>\-([0-9]+).*> энергии извлечено и передано <",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*(?:<localized .*?>)?(.+)\*<",
    },
    "french": {
        "character": "(?<=Auditeur: ).*",
        "sessionTime": "(?<=Session commencée: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?:<localized .*?>)?(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?:<localized .*?>)?(?P<default_ship>.*)\)<|<)/b.*> \-(?: (?:<localized .*?>)?(?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>à<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>de<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> points de blindage transférés à distance à <",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> points de structure transférés à distance à <",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*> points de boucliers transférés à distance à <",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> points de blindage réparés à distance par <",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> points de structure réparés à distance par <",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*> points de boucliers transférés à distance par <",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*> points de capaciteur transférés à distance à <",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*> d'énergie neutralisée en faveur de <",
        "nosRecieved": "\(combat\) <.*?><b>([0-9]+).*> d'énergie siphonnée aux dépens de <",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*> points de capaciteur transférés à distance par <",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>([0-9]+).*> d'énergie neutralisée aux dépens de <",
        "nosTaken": "\(combat\) <.*?><b>([0-9]+).*> d'énergie siphonnée en faveur de <",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*(?:<localized .*?>)?(.+)\*<",
    },
    "german": {
        "character": "(?<=Empfänger: ).*",
        "sessionTime": "(?<=Sitzung gestartet: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?:<localized .*?>)?(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?:<localized .*?>)?(?P<default_ship>.*)\)<|<)/b.*> \-(?: (?:<localized .*?>)?(?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>nach<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>von<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> Panzerungs-Fernreparatur zu <",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> Rumpf-Fernreparatur zu <",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*> Schildfernbooster aktiviert zu <",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> Panzerungs-Fernreparatur von <",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> Rumpf-Fernreparatur von <",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*> Schildfernbooster aktiviert von <",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*> Fernenergiespeicher übertragen zu <",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*> Energie neutralisiert <",
        "nosRecieved": "\(combat\) <.*?><b>\+([0-9]+).*> Energie transferiert von <",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*> Fernenergiespeicher übertragen von <",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>\-([0-9]+).*> Energie neutralisiert <",
        "nosTaken": "\(combat\) <.*?><b>\-([0-9]+).*> Energie transferiert zu <",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*(?:<localized .*?>)?(.+)\*<",
    },
    "japanese": {
        "character": "(?<=傍聴者: ).*",
        "sessionTime": "(?<=セッション開始: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?:<localized .*?>)?(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?:<localized .*?>)?(?P<default_ship>.*)\)<|<)/b.*> \-(?: (?:<localized .*?>)?(?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>対象:<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>攻撃者:<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> remote armor repaired to <",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*> remote hull repaired to <",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*> remote shield boosted to <",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> remote armor repaired by <",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*> remote hull repaired by <",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*> remote shield boosted by <",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*> remote capacitor transmitted to <",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*> エネルギーニュートラライズ 対象:<",
        "nosRecieved": "\(combat\) <.*?><b>\+([0-9]+).*> エネルギードレイン 対象:<",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*> remote capacitor transmitted by <",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>([0-9]+).*>のエネルギーが解放されました<",
        "nosTaken": "\(combat\) <.*?><b>\-([0-9]+).*> エネルギードレイン 攻撃者:<",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*(?:<localized .*?>)?(.+)\*<",
    },
    "chinese": {
        "character": "(?<=收听者: ).*",
        "sessionTime": "(?<=进程开始: ).*",
        "pilotAndWeapon": "(?:.*ffffffff>(?:<localized .*?>)?(?P<default_pilot>[^\(\)<>]*)(?:\[.*\((?:<localized .*?>)?(?P<default_ship>.*)\)<|<)/b.*> \-(?: (?:<localized .*?>)?(?P<default_weapon>.*?)(?: \-|<)|.*))",
        "damageOut": "\(combat\) <.*?><b>([0-9]+).*>对<",
        "damageIn": "\(combat\) <.*?><b>([0-9]+).*>来自<",
        "armorRepairedOut": "\(combat\) <.*?><b>([0-9]+).*>远程装甲维修量至<",
        "hullRepairedOut": "\(combat\) <.*?><b>([0-9]+).*>远程结构维修量至<",
        "shieldBoostedOut": "\(combat\) <.*?><b>([0-9]+).*>远程护盾回充增量至<",
        "armorRepairedIn": "\(combat\) <.*?><b>([0-9]+).*>远程装甲维修量由<",
        "hullRepairedIn": "\(combat\) <.*?><b>([0-9]+).*>远程结构维修量由<",
        "shieldBoostedIn": "\(combat\) <.*?><b>([0-9]+).*>远程护盾回充增量由<",
        "capTransferedOut": "\(combat\) <.*?><b>([0-9]+).*>远程电容传输至<",
        "capNeutralizedOut": "\(combat\) <.*?ff7fffff><b>([0-9]+).*>能量中和<",
        "nosRecieved": "\(combat\) <.*?><b>\+([0-9]+).*>被从<",
        "capTransferedIn": "\(combat\) <.*?><b>([0-9]+).*>远程电容传输量由<",
        "capNeutralizedIn": "\(combat\) <.*?ffe57f7f><b>([0-9]+).*>能量中和<",
        "nosTaken": "\(combat\) <.*?><b>\-([0-9]+).*>被吸取到<",
        "mined": "\(mining\) .*? <.*?><.*?>([0-9]+).*(?:<localized .*?>)?(.+)\*<",
    },
}
