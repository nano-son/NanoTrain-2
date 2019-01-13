import requests
import sys
import time
from bs4 import BeautifulSoup as bs
from stationCode import stations
from pygame import mixer

id = "id"
pw = "pw"
depart_station = "서울"
arrive_station = "동대구"
train_sort = '00' #열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
number_of_adult = 1
year = '2019' #YYYY
month = '01' #MM
day = '13' #DD (3일이면 03으로 해야함)
reserve_time = '2200' #HHMM으로
# day_of_week = '수' #요일
sleep_time = 5

common_param = {}

login_url ="https://www.letskorail.com/korail/com/loginAction.do"
login_confirm_url = "https://www.letskorail.com/korail/com/loginProc.do"
lookup_url = "https://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do"
reserve_url = "https://www.letskorail.com/ebizprd/EbizPrdTicketPr12111_i1.do"
KTX = "KTX"

cookies = {
    'saveMember': id
}

lookup_param = {
    'selGoTrain': train_sort,
    'txtPsgFlg_1': 1, #n: 어른 수
    'txtPsgFlg_2': 0, #장애 만4세~12세 어린이
    'txtPsgFlg_3': 0, #만 65세 이상
    'txtPsgFlg_4': 0, #장애1~3급
    'txtPsgFlg_5': 0, #장애4~6급
    'txtSeatAttCd_3': 000, #좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd_2': 000, #좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd_4': '015', #세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoTrainRa': train_sort, #열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
    'radJobId': 1, #직통:1, 나머진(환승, 왕복) 귀찮다. 안한다.
    'txtGoStart': depart_station,
    'txtGoEnd': arrive_station,
    'txtGoStartCode': None,
    'txtGoEndCode': None,
    'selGoYear': year,
    'selGoMonth': month, #MM형식으로 맞춰야함
    'selGoDay': day,
    'selGoHour': reserve_time[0:2],
    'txtGoHour': reserve_time.ljust(6, '0'),
    # 'txtGoYoil': day_of_week,
    'selGoSeat1': '015',
    # 'selGoSeat2':,
    'txtPsgCnt1': 1, #전체 사람수 (휠체어 좌석 선택시 전체사람수 - 장애인수)
    'txtPsgCnt2': 0, #장애인 사람
    'txtGoPage': 1, #조회페이지는 1, 예약페이지는2 ??
    'txtGoAbrdDt': year+month+day,
    # 'selGoRoom':,
    # 'useSeatFlg':,
    # 'useServiceFlg':,
    'checkStnNm': 'Y', #???
    'txtMenuId': 11, #??
    # 'SeandYo':,
    # 'txtGoStartCode2':,
    # 'txtGoEndCode2':,
    # 'selGoStartDay':,
    # 'hidEasyTalk':
}

reserve_param = {
    'selGoTrain': train_sort,
    'txtPsgFlg_1': 1, #n: 어른 수
    'txtPsgFlg_2': 0, #장애 만4세~12세 어린이
    'txtPsgFlg_3': 0, #만 65세 이상
    'txtPsgFlg_4': 0, #장애1~3급
    'txtPsgFlg_5': 0, #장애4~6급
    'txtSeatAttCd_3': '000', #좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd_2': '000', #좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd_4': '015', #세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoTrainRa': train_sort, #열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
    'radJobId': 1, #직통:1, 나머진(환승, 왕복) 귀찮다. 안한다.
    'txtGoStart': depart_station,
    'txtGoEnd': arrive_station,
    'selGoYear': year,
    'selGoMonth': month,
    'selGoDay': day,
    # 'txtGoYoil': day_of_week,
    'selGoSeat1': '015', #세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoSeat2': '015', #세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'txtPsgCnt1': 0, #카운트가 이상하지만.. 고정인듯
    'txtPsgCnt2': 0, #카운트가 이상하지만.. 고정인듯
    'txtGoPage': 1, #?? 고정인듯
    'txtGoAbrdDt': year+month+day, #예약 날짜
    # 'selGoRoom':,
    # 'useSeatFlg':,
    # 'useServiceFlg':,
    'checkStnNm': 'Y', #?? 고정인듯
    # chkBtnImgTrn1:,
    # chkBtnImgTrn2:,
    'chkInitFlg': 'Y', #?? 고정하면 되는 듯
    'txtMenuId': 11, #?? 고정하면 되는 듯
    'ra': 1, #할인카드 사용 여. 고정
    'txtSeatAttCd1': '000', #??
    'txtSeatAttCd2': '000', #좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd3': '000', #좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd4': '015', #세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    # 'txtSeatAttCd4_1':,
    'txtSeatAttCd5': '000', #?? 고정인듯
    'strChkCpn': 'N', #쿠폰사용 여부 체크 (default : N)
    'txtTotPsgCnt': '1', #사람 수
    'txtSrcarCnt': '0', #?? 고정인듯
    'txtSrcarCnt1': '0', #?? 고정인듯
    # 'hidRsvChgNo': None, #?? 고정인듯
    'hidRsvTpCd': '03', #일반 예약:03, 단체예약:09
    'txtPsgTpCd1': '1', #?? 고정인듯
    'txtPsgTpCd2': '3', #?? 고정인듯
    'txtPsgTpCd3': '1', #?? 고정인듯
    # 'txtPsgTpCd4': None, #?? 고정인듯
    'txtPsgTpCd5': '1', #?? 고정인듯
    # 'txtPsgTpCd6': None, #?? 고정인듯
    'txtPsgTpCd7': '1', #?? 고정인듯
    'txtPsgTpCd8': '1', #?? 고정인듯
    'txtPsgTpCd9': '1', #?? 고정인듯
    'txtDiscKndCd1': '000', #?? 고정인듯
    'txtDiscKndCd2': '000', #?? 고정인듯
    'txtDiscKndCd3': '111', #?? 고정인듯
    # 'txtDiscKndCd4': None, #?? 고정인듯
    'txtDiscKndCd5': '131', #?? 고정인듯
    # 'txtDiscKndCd6': None, #?? 고정인듯
    'txtDiscKndCd7': '112', #?? 고정인듯
    # 'txtDiscKndCd8': None, #?? 고정인듯
    # 'txtDiscKndCd9': None, #?? 고정인듯
    'txtCompaCnt1': '1', # 일반 어른
    'txtCompaCnt2': 0, #일반 어린이
    'txtCompaCnt3': 0, #장애1-3 어른
    'txtCompaCnt4': 0, #장애1-3 어린이
    'txtCompaCnt5': 0, #경로 어른
    'txtCompaCnt6': 0, #청소년
    'txtCompaCnt7': 0, #장애4-6 어
    # 'txtCompaCnt8:
    # 'txtCompaCnt9:
    # txtStndFlg:
    'txtJobId': '1101', #개인예약:'1101', 에약대기:'1102', SEATMAP예약:'1103'
    'txtJrnyCnt': '1', #여정 수
    #'txtDptStnConsOrdr1': '000024', #출발역? (열차관련정보) 없어도 됨
    #'txtArvStnConsOrdr1': '000030', #도착역? (열차관련정보) 없어도 됨
    #'txtDptStnRunOrdr1': '000005', #출발..?? (열차관련정보) 없어도 됨
    #'txtArvStnRunOrdr1': '000007', #도착..?? (열차관련정보) 없어도 됨
    # txtDptStnConsOrdr2:
    # txtArvStnConsOrdr2:
    # txtDptStnRunOrdr2:
    # txtArvStnRunOrdr2:
    'txtPsrmClCd1': 1, #일반실:1
    'txtJrnySqno1': '001', #?? 고정인듯
    'txtJrnyTpCd1': '11', #편도:11, 환승:14
    'txtDptDt1': year+month+day, #이렇게 하면 새벽기차는 날짜가 달라질텐데...
    'txtDptRsStnCd1': stations[depart_station], #출발역 코드
    'txtDptRsStnCdNm1': depart_station, #출발역 이름
    'txtDptTm1': '**', #출발시간
    'txtArvRsStnCd1': stations[arrive_station], #도착역 코드
    'txtArvRsStnCdNm1': arrive_station, #도착역 이름
    'txtArvTm1': '**', #도착시간
    'txtTrnNo1': '**', #열차 번호 (열차관련 정보)
    'txtRunDt1': year+month+day, #날짜
    'txtTrnClsfCd1': '00', #?? 고정인듯
    'txtTrnGpCd1': '100', #고정하면될듯..
    'txtChgFlg1': 'N', #?? 고정인듯
}

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
    'UserId': id,
    'UserPwd': pw,
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


def login(id, pw):
    param = dict(login_param)
    param['UserId'] = id
    param['UserPwd'] = pw
    response = requests.post(login_url, headers = login_header, params = param)
    # print('-----login response body----')
    # print(response.text)
    if('비밀번호 5회 오류시 로그인할 수 없습니다' in response.text):
        return False
    if('ret_url' in response.text and 'strWebPwdCphdAt' in response.text and response.cookies['JSESSIONID']):
        cookies['JSESSIONID'] = response.cookies['JSESSIONID']
        return True


# <li class="log_nm">손은호<span><b>님 환영합니다.</b></span><!-- <a href=javascript:goMem() tabindex="2" ></a> --></li>
# <li><a href="#" onclick="return m_logout_link()"><img src="/images/gnb_logout.gif" alt="로그아웃" /></a></li>
def login_confirm():
    header = dict(common_header)
    response = requests.post(login_confirm_url, headers = header, cookies = cookies, params = login_confirm_param)
    if(bs(response.text, 'html.parser').find('li', attrs={"class": "log_nm"})):
        return True
    else:
        return False


#좌석 조회
def lookup():
    print('\n좌석을 조회합니다..')
    header = dict(common_header)
    response = requests.post(lookup_url, headers = header, cookies = cookies, params = lookup_param)

    tr_list = bs(response.text, 'html.parser').select('#tableResult > tr')
    for tr in tr_list:
        td_list = bs(str(tr), 'html.parser').select('td')
        train_type = bs(str(td_list[1]), 'html.parser').find('span').text.strip()
        if(train_type != KTX):
            continue

        depart_time = td_list[2].text.replace(depart_station, ' ').replace(':', '').strip().ljust(6,'0')
        arrive_time = td_list[3].text.replace(arrive_station, ' ').replace(':', '').strip().ljust(6,'0')
        train_number = bs(str(td_list[1]), 'html.parser').find('a').text.strip().rjust(5, '0')
        first_class_seat = td_list[4]
        economy_class_seat = td_list[5]
        child_seat = td_list[6]

        print('train number : {}, depart_time:{}, arrive_time:{}'.format(train_number, depart_time, arrive_time))

        if '예약하기' in str(economy_class_seat):
            #예약 가능한 객체 정보를 리턴하자.
            print('train number:{} 예약 가능. 시도해보겠음'.format(train_number))
            print('--------')
            if reserve(depart_time, arrive_time, train_number):
                return True
    return False


def reserve(depart_time, arrive_time, train_number):
    # if('238' not in train_number):
    #     return False

    print('[reserve] train number : {}, depart_time:{}, arrive_time:{}'.format(train_number, depart_time, arrive_time))
    header = dict(common_header)
    success_msg = "alert('20분 이내 결제하셔야 승차권 구매가 완료됩니다.')"
    reserve_param['txtTrnNo1'] = train_number
    reserve_param['txtDptTm1'] = depart_time
    reserve_param['txtArvTm1'] = arrive_time
    header['Referer'] = 'http://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do'
    print('reserver_param-----------')
    print(reserve_param)

    response = requests.post(reserve_url, headers=header, cookies=cookies, params=reserve_param)

    print(response.text)
    print('------==========------')
    if(response.status_code == 200 and success_msg in response.text):
        print('20분 이내 결제하셔야 승차권 구매가 완료됩니다.')
        return True
    return False


def validate_setting_info():
    #날짜, 시간 체크
    #역 체크
    return True


def announce_success():
    for i in range(1, 4):
        mixer.init()
        mixer.music.load('gunshot.mp3')
        # wait for load
        time.sleep(1)
        # wait for load
        time.sleep(1)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
    print("done")

def shutdown():
    sys.exit(1)

######################################################################
#########################    MAIN LOGIC    ###########################
######################################################################


if not validate_setting_info():
    print("setting info check plz")
    shutdown()


if login(id, pw) and login_confirm():
    print('***[ LOGIN SUCCESS ]')
else:
    print('***[ LOGIN FAIL ]')
    sys.exit(1)

while True:
    result = lookup()
    if(result):
        print('---------예약성공---------')
        announce_success()
        sys.exit(0)
    time.sleep(sleep_time)


