login_url ="https://www.letskorail.com/korail/com/loginAction.do"
login_confirm_url = "https://www.letskorail.com/korail/com/loginProc.do"
lookup_url = "https://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do"
reserve_url = "https://www.letskorail.com/ebizprd/EbizPrdTicketPr12111_i1.do"
KTX = "KTX"

login_header = {
    'Host' : 'www.letskorail.com',
    # 'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0",
    'Accept' : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.letskorail.com/korail/com/login.do',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

common_header = {
    'Host': 'www.letskorail.com',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive'
}

login_param = {
    'selInputFlg': 2, #로그인 타입 (회원번호==2, 전화번호==4)
    'radIngrDvCd': 2,
    'hidMemberFlg': 1,
    'txtDv': 2,
    # 'UserId': id,
    # 'UserPwd': pw,

    # 'encUserId' : None,
    # 'encUserPwd' : None,
    # 'keyname' : 21,
    #아래 5개는 없어도 되지만 그냥 남긴다.
    'acsURI': 'http://www.letskorail.com:80/ebizsso/sso/acs',
    'providerName': 'Ebiz Sso',
    'forwardingURI': '/ebizsso/sso/sp/service_proc.jsp',
    'RelayState': '/ebizsso/sso/sp/service_front.jsp',
    'IPType' : 'Ebiz Sso Identity Provider'
}

login_confirm_param ={
    'ret_url': '/',
    'strWebPwdCphdAt': 'Y'
}

reserv_success_msg = "20분 이내 결제하셔야 승차권 구매가 완료됩니다"
reserv_time_limit_msg = "20분 이내 열차는 예약하실 수 없습니다"



def make_login_param(id, pw):
    login_param['UserId'] = id
    login_param['UserPwd'] = pw
    return login_param