# encoding: utf-8

APPS = None

def get_app_name(app_id):
    global APPS
    if not APPS:
        APPS = dict(APP_LIST)
    return APPS.get(app_id, app_id)
    
APP_LIST = [
        ("1:34", "3pc"),
        ("1:107", "an"),
        ("1:61", "any-host-internal"),
        ("1:13", "argus"),
        ("1:104", "aris"),
        ("1:93", "ax25"),
        ("1:10", "bbnrccmon"),
        ("1:49", "bna"),
        ("1:76", "br-sat-mon"),
        ("1:7", "cbt"),
        ("1:62", "cftp"),
        ("1:16", "chaos"),
        ("1:110", "compaq-peer"),
        ("1:73", "cphb"),
        ("1:72", "cpnx"),
        ("1:126", "crtp"),
        ("1:127", "crudp"),
        ("1:33", "dccp"),
        ("1:19", "dcn-meas"),
        ("1:37", "ddp"),
        ("1:116", "ddx"),
        ("1:86", "dgp"),
        ("1:48", "dsr"),
        ("1:8", "egp"),
        ("1:88", "eigrp"),
        ("1:14", "emcon"),
        ("1:98", "encap"),
        ("1:97", "etherip"),
        ("1:133", "fc"),
        ("1:125", "fire"),
        ("1:3", "ggp"),
        ("1:100", "gmtp"),
        ("1:47", "gre"),
        ("1:139", "hip"),
        ("1:20", "hmp"),
        ("1:0", "hopopt"),
        ("1:52", "i-nlsp"),
        ("1:117", "iatp"),
        ("1:1", "icmp"),
        ("1:35", "idpr"),
        ("1:38", "idpr-cmtp"),
        ("1:45", "idrp"),
        ("1:101", "ifmp"),
        ("1:9", "igrp"),
        ("1:40", "il"),
        ("1:108", "ipcomp"),
        ("1:71", "ipcv"),
        ("1:4", "ipinip"),
        ("1:94", "ipip"),
        ("1:129", "iplt"),
        ("1:67", "ippc"),
        ("1:44", "ipv6-frag"),
        ("1:58", "ipv6-icmp"),
        ("1:59", "ipv6-nonxt"),
        ("1:60", "ipv6-opts"),
        ("1:43", "ipv6-route"),
        ("1:41", "ipv6inip"),
        ("1:111", "ipx-in-ip"),
        ("1:28", "irtp"),
        ("1:124", "isis"),
        ("1:29", "iso-tp4"),
        ("1:115", "l2tp"),
        ("1:91", "larp"),
        ("1:25", "leaf-1"),
        ("1:26", "leaf-2"),
        ("1:138", "manet"),
        ("1:32", "merit-inp"),
        ("1:31", "mfe-nsp"),
        ("1:95", "micp"),
        ("1:55", "mobile"),
        ("1:137", "mpls-in-ip"),
        ("1:92", "mtp"),
        ("1:18", "mux"),
        ("1:54", "narp"),
        ("1:30", "netblt"),
        ("1:85", "nsfnet-igp"),
        ("1:11", "nvp-ii"),
        ("1:89", "ospf"),
        ("1:113", "pgm"),
        ("1:103", "pim"),
        ("1:131", "pipe"),
        ("1:102", "pnni"),
        ("1:21", "prm"),
        ("1:123", "ptp"),
        ("1:12", "pup"),
        ("1:75", "pvp"),
        ("1:106", "qnx"),
        ("1:27", "rdp"),
        ("1:46", "rsvp"),
        ("1:134", "rsvp-e2e-ignore"),
        ("1:66", "rvd"),
        ("1:64", "sat-expak"),
        ("1:69", "sat-mon"),
        ("1:96", "scc-sp"),
        ("1:118", "schedule-transfer"),
        ("1:105", "scps"),
        ("1:132", "sctp"),
        ("1:42", "sdrp"),
        ("1:82", "secure-vmtp"),
        ("1:57", "skip"),
        ("1:122", "sm"),
        ("1:121", "smp"),
        ("1:109", "snp"),
        ("1:90", "sprite-rpc"),
        ("1:130", "sps"),
        ("1:119", "srp"),
        ("1:128", "sscopmce"),
        ("1:5", "st"),
        ("1:77", "sun-nd"),
        ("1:53", "swipe"),
        ("1:87", "tcf"),
        ("1:56", "tlsp"),
        ("1:39", "tp++"),
        ("1:23", "trunk-1"),
        ("1:24", "trunk-2"),
        ("1:84", "ttp"),
        ("1:136", "udplite"),
        ("1:120", "uti"),
        ("1:70", "visa"),
        ("1:81", "vmtp"),
        ("1:112", "vrrp"),
        ("1:79", "wb-expak"),
        ("1:78", "wb-mon"),
        ("1:74", "wsn"),
        ("1:15", "xnet"),
        ("1:22", "xns-idp"),
        ("1:36", "xtp"),
        ("3:629", "3com-amp3"),
        ("3:106", "3com-tsmux"),
        ("3:211", "914c/g"),
        ("3:564", "9pfs"),
        ("3:216", "CAIlic"),
        ("3:6085", "Konspire2b"),
        ("3:6997", "MobilitySrv"),
        ("3:674", "acap"),
        ("3:62", "acas"),
        ("3:888", "accessbuilder"),
        ("3:699", "accessnetwork"),
        ("3:599", "acp"),
        ("3:104", "acr-nema"),
        ("3:149", "aed-512"),
        ("3:548", "afpovertcp"),
        ("3:705", "agentx"),
        ("3:463", "alpes"),
        ("3:10080", "amanda"),
        ("3:2639", "aminet"),
        ("3:212", "anet"),
        ("3:116", "ansanotify"),
        ("3:124", "ansatrader"),
        ("3:654", "aodv"),
        ("3:5190", "aol-protocol"),
        ("3:2160", "apc-powerchute"),
        ("3:539", "apertus-ldp"),
        ("3:3283", "apple-remote-desktop"),
        ("3:9022", "applejuice"),
        ("3:458", "appleqtc"),
        ("3:545", "appleqtcsrvr"),
        ("3:262", "arcisdms"),
        ("3:419", "ariel1"),
        ("3:421", "ariel2"),
        ("3:422", "ariel3"),
        ("3:384", "arns"),
        ("3:8211", "aruba-papi"),
        ("3:449", "as-servermap"),
        ("3:386", "asa"),
        ("3:502", "asa-appl-proto"),
        ("3:311", "asip-webadmin"),
        ("3:687", "asipregistry"),
        ("3:203", "at-3"),
        ("3:205", "at-5"),
        ("3:207", "at-7"),
        ("3:208", "at-8"),
        ("3:204", "at-echo"),
        ("3:202", "at-nbp"),
        ("3:201", "at-rtmp"),
        ("3:206", "at-zis"),
        ("3:182", "audit"),
        ("3:48", "auditd"),
        ("3:364", "aurora-cmgr"),
        ("3:387", "aurp"),
        ("3:113", "auth"),
        ("3:486", "avian"),
        ("3:3211", "avocent"),
        ("3:47808", "bacnet"),
        ("3:567", "banyan-rpc"),
        ("3:573", "banyan-vip"),
        ("3:1984", "bb"),
        ("3:581", "bdp"),
        ("3:152", "bftp"),
        ("3:264", "bgmp"),
        ("3:179", "bgp"),
        ("3:482", "bgs-nsi"),
        ("3:357", "bhevent"),
        ("3:248", "bhfhs"),
        ("3:310", "bhmds"),
        ("3:142", "bl-idm"),
        ("3:3724", "blizwow"),
        ("3:632", "bmpp"),
        ("3:415", "bnet"),
        ("3:707", "borland-dsj"),
        ("3:595", "cab-protocol"),
        ("3:282", "cableport-ax"),
        ("3:770", "cadlock"),
        ("3:20500", "call-of-duty"),
        ("3:5246", "capwap-control"),
        ("3:5247", "capwap-data"),
        ("3:223", "cdc"),
        ("3:8880", "cddbp-alt"),
        ("3:120", "cfdptkt"),
        ("3:19", "chargen"),
        ("3:18190", "checkpoint-cpmi"),
        ("3:562", "chshell"),
        ("3:673", "cimplex"),
        ("3:130", "cisco-fna"),
        ("3:8905", "cisco-nac"),
        ("3:132", "cisco-sys"),
        ("3:711", "cisco-tdp"),
        ("3:131", "cisco-tna"),
        ("3:1604", "citrix-static"),
        ("3:371", "clearcase"),
        ("3:356", "cloanto-net-1"),
        ("3:164", "cmip-agent"),
        ("3:163", "cmip-man"),
        ("3:1529", "coauthor"),
        ("3:370", "codaauth2"),
        ("3:622", "collaborator"),
        ("3:542", "commerce"),
        ("3:2", "compressnet"),
        ("3:437", "comscm"),
        ("3:759", "con"),
        ("3:531", "conference"),
        ("3:693", "connendp"),
        ("3:3365", "contentserver"),
        ("3:6499", "cooltalk"),
        ("3:683", "corba-iiop"),
        ("3:684", "corba-iiop-ssl"),
        ("3:284", "corerjd"),
        ("3:530", "courier"),
        ("3:64", "covia"),
        ("3:2301", "cpq-wbem"),
        ("3:455", "creativepartnr"),
        ("3:453", "creativeserver"),
        ("3:507", "crs"),
        ("3:624", "cryptoadmin"),
        ("3:348", "csi-sgwp"),
        ("3:105", "csnet-ns"),
        ("3:84", "ctf"),
        ("3:528", "custix"),
        ("3:442", "cvc_hostd"),
        ("3:2401", "cvspserver"),
        ("3:5999", "cvsup"),
        ("3:551", "cybercash"),
        ("3:763", "cycleserv"),
        ("3:772", "cycleserv2"),
        ("3:497", "dantz"),
        ("3:439", "dasp"),
        ("3:461", "datasurfsrv"),
        ("3:462", "datasurfsrvsec"),
        ("3:355", "datex-asn"),
        ("3:13", "daytime"),
        ("3:217", "dbase"),
        ("3:6305", "dclink"),
        ("3:93", "dcp"),
        ("3:675", "dctp"),
        ("3:447", "ddm-dfm"),
        ("3:446", "ddm-rdb"),
        ("3:448", "ddm-ssl"),
        ("3:625", "dec_dlm"),
        ("3:403", "decap"),
        ("3:316", "decauth"),
        ("3:579", "decbsrv"),
        ("3:410", "decladebug"),
        ("3:441", "decvms-sysmgt"),
        ("3:618", "dei-icda"),
        ("3:76", "deos"),
        ("3:52300", "desknets"),
        ("3:801", "device"),
        ("3:647", "dhcp-failover"),
        ("3:847", "dhcp-failover2"),
        ("3:546", "dhcpv6-client"),
        ("3:547", "dhcpv6-server"),
        ("3:466", "digital-vrc"),
        ("3:2234", "directplay"),
        ("3:6073", "directplay8"),
        ("3:3337", "directv-catlg"),
        ("3:3335", "directv-soft"),
        ("3:3336", "directv-tick"),
        ("3:3334", "directv-web"),
        ("3:9", "discard"),
        ("3:667", "disclose"),
        ("3:3632", "distcc"),
        ("3:96", "dixie"),
        ("3:197", "dls"),
        ("3:198", "dls-mon"),
        ("3:195", "dn6-nlm-aud"),
        ("3:436", "dna-cml"),
        ("3:20000", "dnp"),
        ("3:53", "dns"),
        ("3:90", "dnsix"),
        ("3:666", "doom"),
        ("3:315", "dpsi"),
        ("3:17500", "dropbox"),
        ("3:438", "dsfgw"),
        ("3:33", "dsp"),
        ("3:246", "dsp3270"),
        ("3:352", "dtag-ste-sb"),
        ("3:365", "dtk"),
        ("3:644", "dwr"),
        ("3:7", "echo"),
        ("3:704", "elcsd"),
        ("3:394", "embl-ndt"),
        ("3:141", "emfis-cntl"),
        ("3:140", "emfis-data"),
        ("3:775", "entomb"),
        ("3:680", "entrust-aaas"),
        ("3:681", "entrust-aams"),
        ("3:710", "entrust-ash"),
        ("3:709", "entrust-kmsh"),
        ("3:640", "entrust-sps"),
        ("3:135", "epmap"),
        ("3:121", "erpc"),
        ("3:621", "escp-ip"),
        ("3:2189", "esignal"),
        ("3:642", "esro-emsdp"),
        ("3:259", "esro-gen"),
        ("3:592", "eudora-set"),
        ("3:512", "exec"),
        ("3:347", "fatserv"),
        ("3:510", "fcp"),
        ("3:2399", "filemaker-announcement"),
        ("3:79", "finger"),
        ("3:744", "flexlm"),
        ("3:221", "fln-spx"),
        ("3:7100", "font-service"),
        ("3:21", "ftp"),
        ("3:574", "ftp-agent"),
        ("3:20", "ftp-data"),
        ("3:989", "ftps-data"),
        ("3:747", "fujitsu-dev"),
        ("3:190", "gacp"),
        ("3:538", "gdomap"),
        ("3:3050", "gds_db"),
        ("3:402", "genie"),
        ("3:176", "genrad-mux"),
        ("3:678", "ggf-ncp"),
        ("3:634", "ginad"),
        ("3:19150", "gkrellm"),
        ("3:491", "go-login"),
        ("3:5325", "goboogy"),
        ("3:70", "gopher"),
        ("3:2217", "gotodevice"),
        ("3:41", "graphics"),
        ("3:2492", "groove"),
        ("3:1677", "groupwise"),
        ("3:2811", "gsiftp"),
        ("3:488", "gss-http"),
        ("3:128", "gss-xlicen"),
        ("3:2152", "gtp-user"),
        ("3:694", "ha-cluster"),
        ("3:12975", "hamachi"),
        ("3:661", "hap"),
        ("3:375", "hassle"),
        ("3:686", "hcp-wismar"),
        ("3:263", "hdap"),
        ("3:652", "hello-port"),
        ("3:151", "hems"),
        ("3:7220", "heroix-longitude"),
        ("3:20016", "hitachi-spc"),
        ("3:612", "hmmp-ind"),
        ("3:613", "hmmp-op"),
        ("3:101", "hostname"),
        ("3:383", "hp-alarm-mgr"),
        ("3:381", "hp-collector"),
        ("3:382", "hp-managed-node"),
        ("3:9100", "hp-pdl-datastr"),
        ("3:80", "http"),
        ("3:591", "http-alt"),
        ("3:280", "http-mgmt"),
        ("3:593", "http-rpc-epmap"),
        ("3:473", "hybrid-pop"),
        ("3:418", "hyper-g"),
        ("3:692", "hyperwave-isp"),
        ("3:480", "iafdbase"),
        ("3:479", "iafserver"),
        ("3:432", "iasd"),
        ("3:4569", "iax"),
        ("3:385", "ibm-app"),
        ("3:523", "ibm-db2"),
        ("3:4490", "ibm-director"),
        ("3:6714", "ibprotocol"),
        ("3:886", "iclcnet-locate"),
        ("3:887", "iclcnet_svinfo"),
        ("3:549", "idfp"),
        ("3:651", "ieee-mms"),
        ("3:695", "ieee-mms-ssl"),
        ("3:535", "iiop"),
        ("3:143", "imap"),
        ("3:406", "imsp"),
        ("3:244", "inbusiness"),
        ("3:414", "infoseek"),
        ("3:134", "ingres-net"),
        ("3:495", "intecourier"),
        ("3:484", "integra-sme"),
        ("3:503", "intrinsa"),
        ("3:576", "ipcd"),
        ("3:600", "ipcserver"),
        ("3:578", "ipdd"),
        ("3:631", "ipp"),
        ("3:194", "irc"),
        ("3:529", "irc-serv"),
        ("3:379", "is99c"),
        ("3:380", "is99s"),
        ("3:500", "isakmp"),
        ("3:860", "iscsi"),
        ("3:3260", "iscsi-target"),
        ("3:55", "isi-gl"),
        ("3:499", "iso-ill"),
        ("3:147", "iso-ip"),
        ("3:146", "iso-tp0"),
        ("3:102", "iso-tsap"),
        ("3:399", "iso-tsap-c2"),
        ("3:828", "itm-mcell-s"),
        ("3:148", "jargon"),
        ("3:287", "k-block"),
        ("3:2213", "kali"),
        ("3:88", "kerberos"),
        ("3:749", "kerberos-adm"),
        ("3:584", "keyserver"),
        ("3:186", "kis"),
        ("3:543", "klogin"),
        ("3:157", "knet-cmp"),
        ("3:464", "kpasswd"),
        ("3:398", "kryptolan"),
        ("3:544", "kshell"),
        ("3:51", "la-maint"),
        ("3:637", "lanserver"),
        ("3:389", "ldap"),
        ("3:646", "ldp"),
        ("3:373", "legent-1"),
        ("3:374", "legent-2"),
        ("3:472", "ljk-login"),
        ("3:4045", "lockd"),
        ("3:127", "locus-con"),
        ("3:125", "locus-map"),
        ("3:513", "login"),
        ("3:4514", "loglogic"),
        ("3:1352", "lotus-notes"),
        ("3:660", "mac-srvr-admin"),
        ("3:313", "magenta-logic"),
        ("3:505", "mailbox-lm"),
        ("3:174", "mailq"),
        ("3:997", "maitrd"),
        ("3:224", "masqdialer"),
        ("3:350", "matip-type-a"),
        ("3:351", "matip-type-b"),
        ("3:7210", "maxdb"),
        ("3:8801", "mcafee-update"),
        ("3:112", "mcidas"),
        ("3:638", "mcns-sec"),
        ("3:685", "mdc-portmapper"),
        ("3:668", "mecomm"),
        ("3:669", "meregister"),
        ("3:393", "meta5"),
        ("3:99", "metagram"),
        ("3:570", "meter"),
        ("3:86", "mfcobol"),
        ("3:349", "mftp"),
        ("3:490", "micom-pfs"),
        ("3:1534", "micromuse-lm"),
        ("3:445", "microsoftds"),
        ("3:91", "mit-dov"),
        ("3:83", "mit-ml-dev"),
        ("3:434", "mobileip-agent"),
        ("3:435", "mobilip-mn"),
        ("3:471", "mondex"),
        ("3:561", "monitor"),
        ("3:367", "mortgageware"),
        ("3:45", "mpm"),
        ("3:44", "mpm-flags"),
        ("3:46", "mpm-snd"),
        ("3:218", "mpp"),
        ("3:397", "mptn"),
        ("3:679", "mrm"),
        ("3:6891", "ms-ocs-file-transfer"),
        ("3:2393", "ms-olap"),
        ("3:569", "ms-rome"),
        ("3:568", "ms-shuttle"),
        ("3:1434", "ms-sql-m"),
        ("3:1755", "ms-streaming"),
        ("3:3389", "ms-wbt"),
        ("3:639", "msdp"),
        ("3:691", "msexch-routing"),
        ("3:3268", "msft-gc"),
        ("3:3269", "msft-gc-ssl"),
        ("3:31", "msg-auth"),
        ("3:29", "msg-icp"),
        ("3:1863", "msnp"),
        ("3:18", "msp"),
        ("3:777", "multiling-http"),
        ("3:171", "multiplex"),
        ("3:188", "mumps"),
        ("3:467", "mylex-mapd"),
        ("3:3306", "mysql"),
        ("3:42", "name"),
        ("3:167", "namp"),
        ("3:991", "nas"),
        ("3:404", "nced"),
        ("3:405", "ncld"),
        ("3:524", "ncp"),
        ("3:1521", "ncube-lm"),
        ("3:10000", "ndmp"),
        ("3:353", "ndsauth"),
        ("3:489", "nest-protocol"),
        ("3:3300", "net-assistant"),
        ("3:1830", "net8-cman"),
        ("3:138", "netbios-dgm"),
        ("3:137", "netbios-ns"),
        ("3:139", "netbios-ssn"),
        ("3:741", "netgw"),
        ("3:532", "netnews"),
        ("3:1970", "netop-remote-control"),
        ("3:742", "netrcs"),
        ("3:71", "netrjs-1"),
        ("3:72", "netrjs-2"),
        ("3:73", "netrjs-3"),
        ("3:74", "netrjs-4"),
        ("3:155", "netsc-dev"),
        ("3:154", "netsc-prod"),
        ("3:729", "netviewdm1"),
        ("3:730", "netviewdm2"),
        ("3:731", "netviewdm3"),
        ("3:33435", "netvmg-traceroute"),
        ("3:533", "netwall"),
        ("3:396", "netware-ip"),
        ("3:550", "new-rwho"),
        ("3:178", "nextstep"),
        ("3:2049", "nfs"),
        ("3:47", "ni-ftp"),
        ("3:61", "ni-mail"),
        ("3:43", "nicname"),
        ("3:758", "nlogin"),
        ("3:689", "nmap"),
        ("3:537", "nmsp"),
        ("3:433", "nnsp"),
        ("3:119", "nntp"),
        ("3:308", "novastorbakcup"),
        ("3:611", "npmp-gui"),
        ("3:610", "npmp-local"),
        ("3:609", "npmp-trap"),
        ("3:92", "npp"),
        ("3:607", "nqs"),
        ("3:760", "ns"),
        ("3:261", "nsiiops"),
        ("3:359", "nsrmp"),
        ("3:159", "nss-routing"),
        ("3:27", "nsw-fe"),
        ("3:518", "ntalk"),
        ("3:123", "ntp"),
        ("3:126", "nxedit"),
        ("3:650", "obex"),
        ("3:94", "objcall"),
        ("3:183", "ocbinder"),
        ("3:429", "ocs_amu"),
        ("3:428", "ocs_cmu"),
        ("3:184", "ocserver"),
        ("3:366", "odmr"),
        ("3:506", "ohimsrv"),
        ("3:698", "olsr"),
        ("3:900", "omginitialrefs"),
        ("3:5723", "omhs"),
        ("3:764", "omserv"),
        ("3:417", "onmux"),
        ("3:536", "opalis-rdv"),
        ("3:314", "opalis-robot"),
        ("3:423", "opc-job-start"),
        ("3:424", "opc-job-track"),
        ("3:260", "openport"),
        ("3:557", "openvms-sysipc"),
        ("3:1270", "opsmgr"),
        ("3:1525", "ora-srv"),
        ("3:9703", "oracle-bi"),
        ("3:66", "oracle-sqlnet"),
        ("3:1575", "oraclenames"),
        ("3:1630", "oraclenet8cman"),
        ("3:3078", "orbix-cfg-ssl"),
        ("3:3076", "orbix-config"),
        ("3:3077", "orbix-loc-ssl"),
        ("3:3075", "orbix-locator"),
        ("3:192", "osu-nms"),
        ("3:6665", "p10"),
        ("3:6582", "parsec-game"),
        ("3:511", "passgo"),
        ("3:627", "passgo-tivoli"),
        ("3:586", "password-chg"),
        ("3:345", "pawserv"),
        ("3:158", "pcmail-srv"),
        ("3:4172", "pcoip"),
        ("3:344", "pdap"),
        ("3:281", "personal-link"),
        ("3:662", "pftp"),
        ("3:583", "philips-vc"),
        ("3:767", "phonebook"),
        ("3:468", "photuris"),
        ("3:496", "pim-rp-disc"),
        ("3:1321", "pip"),
        ("3:553", "pirp"),
        ("3:829", "pkix-3-ca-ra"),
        ("3:318", "pkix-timestamp"),
        ("3:109", "pop2"),
        ("3:110", "pop3"),
        ("3:5432", "postgresql"),
        ("3:494", "pov-ray"),
        ("3:485", "powerburst"),
        ("3:1723", "pptp"),
        ("3:170", "print-srv"),
        ("3:515", "printer"),
        ("3:409", "prm-nm"),
        ("3:408", "prm-sm"),
        ("3:136", "profile"),
        ("3:191", "prospero"),
        ("3:2351", "psrserver"),
        ("3:597", "ptcnameservice"),
        ("3:319", "ptp-event"),
        ("3:320", "ptp-general"),
        ("3:751", "pump"),
        ("3:663", "purenoise"),
        ("3:129", "pwdgen"),
        ("3:368", "qbikgdp"),
        ("3:189", "qft"),
        ("3:628", "qmqp"),
        ("3:209", "qmtp"),
        ("3:17", "qotd"),
        ("3:752", "qrh"),
        ("3:762", "quotad"),
        ("3:1812", "radius"),
        ("3:4899", "radmin-port"),
        ("3:38", "rap"),
        ("3:469", "rcp"),
        ("3:630", "rda"),
        ("3:1571", "rdb-dbs-disp"),
        ("3:6970", "rdt"),
        ("3:50", "re-mail-ck"),
        ("3:688", "realm-rusd"),
        ("3:185", "remote-kis"),
        ("3:556", "remotefs"),
        ("3:641", "repcmd"),
        ("3:653", "repscmd"),
        ("3:283", "rescap"),
        ("3:520", "rip"),
        ("3:521", "ripng"),
        ("3:180", "ris"),
        ("3:748", "ris-cm"),
        ("3:5", "rje"),
        ("3:39", "rlp"),
        ("3:635", "rlzdbase"),
        ("3:657", "rmc"),
        ("3:1098", "rmiactivation"),
        ("3:1099", "rmiregistry"),
        ("3:560", "rmonitor"),
        ("3:411", "rmt"),
        ("3:369", "rpc2portmap"),
        ("3:753", "rrh"),
        ("3:648", "rrp"),
        ("3:222", "rsh-spx"),
        ("3:168", "rsvd"),
        ("3:1698", "rsvp-encap-1"),
        ("3:1699", "rsvp-encap-2"),
        ("3:363", "rsvp_tunnel"),
        ("3:873", "rsync"),
        ("3:107", "rtelnet"),
        ("3:771", "rtip"),
        ("3:554", "rtsp"),
        ("3:322", "rtsps"),
        ("3:696", "rushd"),
        ("3:761", "rxe"),
        ("3:166", "s-net"),
        ("3:487", "saft"),
        ("3:643", "sanity"),
        ("3:582", "scc-security"),
        ("3:617", "sco-dtmgr"),
        ("3:615", "sco-inetmgr"),
        ("3:616", "sco-sysmgr"),
        ("3:598", "sco-websrvrmg3"),
        ("3:620", "sco-websrvrmgr"),
        ("3:457", "scohelp"),
        ("3:360", "scoi2odialog"),
        ("3:470", "scx-proxy"),
        ("3:558", "sdnskmp"),
        ("3:990", "secure-ftp"),
        ("3:443", "secure-http"),
        ("3:993", "secure-imap"),
        ("3:994", "secure-irc"),
        ("3:636", "secure-ldap"),
        ("3:563", "secure-nntp"),
        ("3:995", "secure-pop3"),
        ("3:992", "secure-telnet"),
        ("3:361", "semantix"),
        ("3:169", "send"),
        ("3:213", "server-ipx"),
        ("3:633", "servstat"),
        ("3:257", "set"),
        ("3:6343", "sflow"),
        ("3:452", "sfs-config"),
        ("3:451", "sfs-smp-net"),
        ("3:115", "sftp"),
        ("3:440", "sgcp"),
        ("3:153", "sgmp"),
        ("3:160", "sgmp-traps"),
        ("3:514", "shell"),
        ("3:1626", "shockwave"),
        ("3:358", "shrinkwrap"),
        ("3:498", "siam"),
        ("3:608", "sift-uft"),
        ("3:706", "silc"),
        ("3:5060", "sip"),
        ("3:5061", "sip-tls"),
        ("3:2631", "sitaradir"),
        ("3:2630", "sitaramgmt"),
        ("3:2629", "sitaraserver"),
        ("3:460", "skronk"),
        ("3:122", "smakynet"),
        ("3:3218", "smartpackets"),
        ("3:426", "smartsdp"),
        ("3:901", "smpnameres"),
        ("3:596", "smsd"),
        ("3:413", "smsp"),
        ("3:25", "smtp"),
        ("3:199", "smux"),
        ("3:108", "snagas"),
        ("3:509", "snare"),
        ("3:161", "snmp"),
        ("3:444", "snpp"),
        ("3:580", "sntp-heartbeat"),
        ("3:1080", "socks"),
        ("3:215", "softpc"),
        ("3:19880", "softros-messenger-ft"),
        ("3:572", "sonar"),
        ("3:656", "spmp"),
        ("3:478", "spsc"),
        ("3:150", "sql-net"),
        ("3:9088", "sqlexec"),
        ("3:1700", "sqlnet"),
        ("3:118", "sqlserv"),
        ("3:1433", "sqlserver"),
        ("3:156", "sqlsrv"),
        ("3:200", "src"),
        ("3:193", "srmp"),
        ("3:362", "srssend"),
        ("3:477", "ss7ns"),
        ("3:22", "ssh"),
        ("3:614", "sshell"),
        ("3:266", "sst"),
        ("3:133", "statsrv"),
        ("3:501", "stmf"),
        ("3:566", "streettalk"),
        ("3:3478", "stun-nat"),
        ("3:5349", "stuns"),
        ("3:527", "stx"),
        ("3:89", "su-mit-tg"),
        ("3:587", "submission"),
        ("3:773", "submit"),
        ("3:247", "subntbcst_tftp"),
        ("3:665", "sun-dr"),
        ("3:111", "sunrpc"),
        ("3:95", "supdup"),
        ("3:243", "sur-meas"),
        ("3:1010", "surf"),
        ("3:3690", "svn"),
        ("3:427", "svrloc"),
        ("3:97", "swift-rvf"),
        ("3:1498", "sybase"),
        ("3:412", "synoptics-trap"),
        ("3:392", "synotics-broker"),
        ("3:391", "synotics-relay"),
        ("3:11", "systat"),
        ("3:49", "tacacs"),
        ("3:98", "tacnews"),
        ("3:517", "talk"),
        ("3:3817", "tapeware"),
        ("3:268", "td-replica"),
        ("3:267", "td-service"),
        ("3:40001", "teamsound"),
        ("3:559", "teedtap"),
        ("3:754", "tell"),
        ("3:23", "telnet"),
        ("3:526", "tempo"),
        ("3:658", "tenfold"),
        ("3:7631", "tesla-sys-msg"),
        ("3:333", "texar"),
        ("3:69", "tftp"),
        ("3:492", "ticf-1"),
        ("3:493", "ticf-2"),
        ("3:407", "timbuktu"),
        ("3:37", "time"),
        ("3:525", "timed"),
        ("3:655", "tinc"),
        ("3:1527", "tlisrv"),
        ("3:476", "tn-tl-fd1"),
        ("3:377", "tnETOS"),
        ("3:590", "tns-cml"),
        ("3:594", "tpip"),
        ("3:11010", "tradestation"),
        ("3:27665", "trinoo"),
        ("3:450", "tserver"),
        ("3:145", "uaac"),
        ("3:219", "uarps"),
        ("3:390", "uis"),
        ("3:372", "ulistproc"),
        ("3:522", "ulp"),
        ("3:483", "ulpnet"),
        ("3:388", "unidata-ldm"),
        ("3:181", "unify"),
        ("3:401", "ups"),
        ("3:606", "urm"),
        ("3:519", "utime"),
        ("3:431", "utmpcd"),
        ("3:430", "utmpsd"),
        ("3:540", "uucp"),
        ("3:117", "uucp-path"),
        ("3:541", "uucp-rlogin"),
        ("3:697", "uuidgen"),
        ("3:671", "vacdsm-app"),
        ("3:670", "vacdsm-sws"),
        ("3:690", "vatp"),
        ("3:575", "vemmi"),
        ("3:769", "vid"),
        ("3:516", "videotex"),
        ("3:1533", "virtual-places"),
        ("3:175", "vmnet"),
        ("3:214", "vmpwscs"),
        ("3:8182", "vmware-fdm"),
        ("3:577", "vnas"),
        ("3:677", "vpp"),
        ("3:672", "vpps-qua"),
        ("3:676", "vpps-via"),
        ("3:996", "vsinet"),
        ("3:312", "vslmp"),
        ("3:2948", "wap-push"),
        ("3:4035", "wap-push-http"),
        ("3:4036", "wap-push-https"),
        ("3:2949", "wap-pushsecure"),
        ("3:9205", "wap-vcal"),
        ("3:9207", "wap-vcal-s"),
        ("3:9204", "wap-vcard"),
        ("3:9206", "wap-vcard-s"),
        ("3:9200", "wap-wsp"),
        ("3:9202", "wap-wsp-s"),
        ("3:9201", "wap-wsp-wtp"),
        ("3:9203", "wap-wsp-wtp-s"),
        ("3:5330", "war-rock"),
        ("3:2048", "wccp"),
        ("3:15868", "websense"),
        ("3:765", "webster"),
        ("3:565", "whoami"),
        ("3:63", "whois++"),
        ("3:2887", "wlccp"),
        ("3:2595", "worldfusion"),
        ("3:780", "wpgs"),
        ("3:265", "x-bone-ctl"),
        ("3:911", "xact-backup"),
        ("3:177", "xdmcp"),
        ("3:3088", "xdtp"),
        ("3:82", "xfer"),
        ("3:25999", "xfire"),
        ("3:5222", "xmpp-client"),
        ("3:56", "xns-auth"),
        ("3:54", "xns-ch"),
        ("3:165", "xns-courier"),
        ("3:58", "xns-mail"),
        ("3:52", "xns-time"),
        ("3:508", "xvttp"),
        ("3:6000", "xwindows"),
        ("3:173", "xyplex-mux"),
        ("3:210", "z39.50"),
        ("3:317", "zannet"),
        ("3:346", "zserv"),
        ("13:0", "unclassified"),
        ("13:1", "unknown"),
        ("13:473", "active-directory"),
        ("13:490", "activesync"),
        ("13:505", "adobe-connect"),
        ("13:549", "airplay"),
        ("13:581", "aliwangwang"),
        ("13:587", "android-updates"),
        ("13:79", "aol-messenger"),
        ("13:500", "aol-messenger-audio"),
        ("13:502", "aol-messenger-ft"),
        ("13:501", "aol-messenger-video"),
        ("13:588", "apple-app-store"),
        ("13:586", "apple-ios-updates"),
        ("13:577", "apple-services"),
        ("13:593", "apple-tv-updates"),
        ("13:264", "applix"),
        ("13:565", "ares"),
        ("13:430", "audio-over-http"),
        ("13:327", "ayiya-ipv6-tunneled"),
        ("13:454", "babelgum"),
        ("13:442", "baidu-movie"),
        ("13:431", "binary-over-http"),
        ("13:69", "bittorrent"),
        ("13:543", "bittorrent-networking"),
        ("13:525", "blogger"),
        ("13:80", "cifs"),
        ("13:456", "cisco-ip-camera"),
        ("13:558", "cisco-jabber-audio"),
        ("13:556", "cisco-jabber-control"),
        ("13:557", "cisco-jabber-im"),
        ("13:561", "cisco-jabber-video"),
        ("13:81", "cisco-phone"),
        ("13:56", "citrix"),
        ("13:582", "consumer-cloud-storage"),
        ("13:12", "cuseeme"),
        ("13:547", "dameware-mrc"),
        ("13:13", "dhcp"),
        ("13:439", "dht"),
        ("13:76", "dicom"),
        ("13:70", "directconnect"),
        ("13:492", "dmp"),
        ("13:67", "edonkey"),
        ("13:416", "edonkey-static"),
        ("13:313", "encrypted-bittorrent"),
        ("13:417", "encrypted-emule"),
        ("13:551", "espn-browsing"),
        ("13:552", "espn-video"),
        ("13:49", "exchange"),
        ("13:518", "facebook"),
        ("13:535", "facetime"),
        ("13:57", "fasttrack"),
        ("13:467", "fasttrack-static"),
        ("13:580", "fc2"),
        ("13:433", "filetopia"),
        ("13:74", "fix"),
        ("13:299", "flash-video"),
        ("13:300", "flashmyspace"),
        ("13:301", "flashyahoo"),
        ("13:54", "fring"),
        ("13:60", "fring-video"),
        ("13:444", "fring-voip"),
        ("13:506", "game-spy"),
        ("13:530", "gbridge"),
        ("13:503", "ghostsurf"),
        ("13:462", "gmail"),
        ("13:58", "gnutella"),
        ("13:528", "google-accounts"),
        ("13:522", "google-docs"),
        ("13:441", "google-earth"),
        ("13:589", "google-play"),
        ("13:521", "google-plus"),
        ("13:520", "google-services"),
        ("13:499", "gotomypc"),
        ("13:451", "gridftp"),
        ("13:470", "gtalk"),
        ("13:464", "gtalk-chat"),
        ("13:308", "gtalk-ft"),
        ("13:471", "gtalk-video"),
        ("13:305", "gtalk-voip"),
        ("13:436", "guruguru"),
        ("13:64", "h323"),
        ("13:73", "hl7"),
        ("13:511", "hotmail"),
        ("13:595", "htc-services"),
        ("13:458", "hulu"),
        ("13:564", "icloud"),
        ("13:269", "icq"),
        ("13:311", "icq-filetransfer"),
        ("13:575", "internet-audio-streaming"),
        ("13:574", "internet-video-streaming"),
        ("13:475", "ip-messenger"),
        ("13:9", "ipsec"),
        ("13:329", "isatap-ipv6-tunneled"),
        ("13:434", "itunes"),
        ("13:571", "itunes-audio"),
        ("13:572", "itunes-video"),
        ("13:583", "kakao-services"),
        ("13:579", "kakao-talk"),
        ("13:59", "kazaa2"),
        ("13:591", "keyholetv"),
        ("13:437", "kuro"),
        ("13:527", "linkedin"),
        ("13:474", "livemeeting"),
        ("13:480", "livestation"),
        ("13:519", "logmein"),
        ("13:378", "lwapp"),
        ("13:585", "mac-os-x-updates"),
        ("13:266", "manolito"),
        ("13:78", "mapi"),
        ("13:448", "maplestory"),
        ("13:459", "megavideo"),
        ("13:62", "mgcp"),
        ("13:514", "mikogo"),
        ("13:592", "mixi"),
        ("13:555", "modbus"),
        ("13:508", "ms-dynamics-crm-online"),
        ("13:482", "ms-iis"),
        ("13:498", "ms-live-accounts"),
        ("13:531", "ms-lync"),
        ("13:559", "ms-lync-audio"),
        ("13:532", "ms-lync-media"),
        ("13:560", "ms-lync-video"),
        ("13:483", "ms-netlogon"),
        ("13:495", "ms-office-365"),
        ("13:563", "ms-office-web-apps"),
        ("13:1310", "ms-rpc"),
        ("13:484", "ms-sms"),
        ("13:497", "ms-update"),
        ("13:481", "ms-win-dns"),
        ("13:75", "msn-messenger"),
        ("13:309", "msn-messenger-ft"),
        ("13:323", "msn-messenger-video"),
        ("13:312", "my-jabber-ft"),
        ("13:268", "napster"),
        ("13:573", "naver-line"),
        ("13:401", "netapp-snapmirror"),
        ("13:26", "netbios"),
        ("13:457", "netflix"),
        ("13:426", "netshow"),
        ("13:420", "networking-gnutella"),
        ("13:2000", "notes"),
        ("13:47", "novadigm"),
        ("13:455", "openvpn"),
        ("13:516", "oracle-ebsuite-unsecured"),
        ("13:513", "oscar-filetransfer"),
        ("13:550", "outlook-web-service"),
        ("13:443", "pando"),
        ("13:515", "pandora"),
        ("13:32", "pcanywhere"),
        ("13:578", "perfect-dark"),
        ("13:486", "perforce"),
        ("13:523", "picasa"),
        ("13:479", "ping"),
        ("13:424", "poco"),
        ("13:423", "ppstream"),
        ("13:542", "pptv"),
        ("13:554", "qq-accounts"),
        ("13:570", "qq-games"),
        ("13:569", "qq-im"),
        ("13:540", "qqlive"),
        ("13:507", "realmedia"),
        ("13:489", "rhapsody"),
        ("13:66", "rtcp"),
        ("13:418", "rtmp"),
        ("13:487", "rtmpe"),
        ("13:491", "rtmpt"),
        ("13:61", "rtp"),
        ("13:566", "rtp-audio"),
        ("13:567", "rtp-video"),
        ("13:509", "salesforce"),
        ("13:84", "sap"),
        ("13:328", "secondlife"),
        ("13:568", "secure-smtp"),
        ("13:576", "share"),
        ("13:488", "share-point"),
        ("13:544", "shoutcast"),
        ("13:534", "showmypc"),
        ("13:330", "sixtofour-ipv6-tunneled"),
        ("13:63", "skinny"),
        ("13:562", "skydrive"),
        ("13:83", "skype"),
        ("13:440", "sling"),
        ("13:450", "songsari"),
        ("13:429", "sopcast"),
        ("13:438", "soribada"),
        ("13:267", "soulseek"),
        ("13:541", "spdy"),
        ("13:453", "ssl"),
        ("13:472", "steam"),
        ("13:427", "streamwork"),
        ("13:379", "synergy"),
        ("13:41", "syslog"),
        ("13:331", "tcpoverdns"),
        ("13:447", "teamspeak"),
        ("13:494", "teamviewer"),
        ("13:114", "telepresence-control"),
        ("13:113", "telepresence-media"),
        ("13:326", "teredo-ipv6-tunneled"),
        ("13:449", "tomatopang"),
        ("13:460", "tor"),
        ("13:435", "tunnel-http"),
        ("13:517", "twitter"),
        ("13:584", "ultrasurf"),
        ("13:1", "unknown"),
        ("13:425", "vdolive"),
        ("13:446", "ventrilo"),
        ("13:1320", "viber"),
        ("13:432", "video-over-http"),
        ("13:476", "vmware-view"),
        ("13:493", "vmware-vmotion"),
        ("13:100", "vnc"),
        ("13:485", "vnc-http"),
        ("13:421", "waste"),
        ("13:546", "webex-app-sharing"),
        ("13:545", "webex-media"),
        ("13:414", "webex-meeting"),
        ("13:445", "webthunder"),
        ("13:553", "whatsapp"),
        ("13:510", "windows-azure"),
        ("13:590", "windows-store"),
        ("13:415", "windows-update"),
        ("13:68", "winmx"),
        ("13:469", "winny"),
        ("13:537", "xunlei"),
        ("13:538", "xunlei-kankan"),
        ("13:533", "yahoo-accounts"),
        ("13:526", "yahoo-mail"),
        ("13:77", "yahoo-messenger"),
        ("13:594", "yahoo-messenger-video"),
        ("13:422", "yahoo-voip-messenger"),
        ("13:1195", "yahoo-voip-over-sip"),
        ("13:82", "youtube"),
        ("13:428", "zattoo")
]
