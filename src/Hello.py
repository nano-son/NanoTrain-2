import requests
import sys
import time
from bs4 import BeautifulSoup as bs
from stationCode import stations
from pygame import mixer
import metaInformation as meta

id = "id"                   #id
pw = "pw"                   #pw
depart_station = "서울"      #출발역
arrive_station = "동대구"      #도착역
train_sort = '00'           # 열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
number_of_adult = 1         # 사람 수 (귀찮아서 성인만 함)
year = '2019'               #예약하고자하는 년도 (YYYY형식)
month = '02'                # 예약하고자하는 월 (MM형식)
day = '04'                  # 예약하고하자는 일 (DD형식) (3일이면 03으로 해야함)
reserve_min_time = '1700'  # HHMM으로
reserve_max_time = '1901'
sleep_time = 5

cookies = {
    'saveMember': id
}

# 좌석 조회 파라미터
# 쓸모 없는 프로퍼티를 많이 지웠다.
lookup_param = {
    'selGoTrain': train_sort,
    'txtPsgFlg_1': 1,  # n: 어른 수
    'txtPsgFlg_2': 0,  # 장애 만4세~12세 어린이
    'txtPsgFlg_3': 0,  # 만 65세 이상
    'txtPsgFlg_4': 0,  # 장애1~3급
    'txtPsgFlg_5': 0,  # 장애4~6급
    'txtSeatAttCd_3': 000,  # 좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd_2': 000,  # 좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd_4': '015',  # 세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoTrainRa': train_sort,  # 열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
    'radJobId': 1,  # 직통:1, 나머진(환승, 왕복) 귀찮다. 안한다.
    'txtGoStart': depart_station,
    'txtGoEnd': arrive_station,
    'txtGoStartCode': None,
    'txtGoEndCode': None,
    'selGoYear': year,
    'selGoMonth': month,  # MM형식으로 맞춰야함
    'selGoDay': day,
    'selGoHour': reserve_min_time[0:2],
    'txtGoHour': reserve_min_time.ljust(6, '0'),
    'selGoSeat1': '015',
    'txtPsgCnt1': 1,  # 전체 사람수 (휠체어 좌석 선택시 전체사람수 - 장애인수)
    'txtPsgCnt2': 0,  # 장애인 사람
    'txtGoPage': 1,  # 조회페이지는 1, 예약페이지는2 ??
    'txtGoAbrdDt': year + month + day,
    'checkStnNm': 'Y',  # ???
    'txtMenuId': 11,  # ??
}


# 예약 파라미터
# 역시 쓸모없는 파라미터를 많이 지웠다.
reserve_param = {
    'selGoTrain': train_sort,
    'txtPsgFlg_1': 1,  # n: 어른 수
    'txtPsgFlg_2': 0,  # 장애 만4세~12세 어린이
    'txtPsgFlg_3': 0,  # 만 65세 이상
    'txtPsgFlg_4': 0,  # 장애1~3급
    'txtPsgFlg_5': 0,  # 장애4~6급
    'txtSeatAttCd_3': '000',  # 좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd_2': '000',  # 좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd_4': '015',  # 세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoTrainRa': train_sort,  # 열차 종류. 전체:05, KTX_SRT:00, ITX_청춘:09, 새마을호/ITX-새마을:08, 무궁화:02, 통근열차:03
    'radJobId': 1,  # 직통:1, 나머진(환승, 왕복) 귀찮다. 안한다.
    'txtGoStart': depart_station,
    'txtGoEnd': arrive_station,
    'selGoYear': year,
    'selGoMonth': month,
    'selGoDay': day,
    'selGoSeat1': '015',  # 세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'selGoSeat2': '015',  # 세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'txtPsgCnt1': 0,  # 카운트가 이상하지만.. 고정인듯
    'txtPsgCnt2': 0,  # 카운트가 이상하지만.. 고정인듯
    'txtGoPage': 1,  # ?? 고정인듯
    'txtGoAbrdDt': year + month + day,  # 예약 날짜
    'checkStnNm': 'Y',  # ?? 고정인듯
    'chkInitFlg': 'Y',  # ?? 고정하면 되는 듯
    'txtMenuId': 11,  # ?? 고정하면 되는 듯
    'ra': 1,  # 할인카드 사용 여. 고정
    'txtSeatAttCd1': '000',  # ??
    'txtSeatAttCd2': '000',  # 좌석반향 전체:000, 순방향:009, 역방향:010
    'txtSeatAttCd3': '000',  # 좌석종류 기본:000, 1인석:011, 창가좌석:012, 내측좌석:013
    'txtSeatAttCd4': '015',  # 세부적인 특징: 기본:015, 노트북 031, 유아동반:019
    'txtSeatAttCd5': '000',  # ?? 고정인듯
    'strChkCpn': 'N',  # 쿠폰사용 여부 체크 (default : N)
    'txtTotPsgCnt': '1',  # 사람 수
    'txtSrcarCnt': '0',  # ?? 고정인듯
    'txtSrcarCnt1': '0',  # ?? 고정인듯
    'hidRsvTpCd': '03',  # 일반 예약:03, 단체예약:09
    'txtPsgTpCd1': '1',  # ?? 고정인듯
    'txtPsgTpCd2': '3',  # ?? 고정인듯
    'txtPsgTpCd3': '1',  # ?? 고정인듯
    'txtPsgTpCd5': '1',  # ?? 고정인듯
    'txtPsgTpCd7': '1',  # ?? 고정인듯
    'txtPsgTpCd8': '1',  # ?? 고정인듯
    'txtPsgTpCd9': '1',  # ?? 고정인듯
    'txtDiscKndCd1': '000',  # ?? 고정인듯
    'txtDiscKndCd2': '000',  # ?? 고정인듯
    'txtDiscKndCd3': '111',  # ?? 고정인듯
    'txtDiscKndCd5': '131',  # ?? 고정인듯
    'txtDiscKndCd7': '112',  # ?? 고정인듯
    'txtCompaCnt1': '1',  # 일반 어른
    'txtCompaCnt2': 0,  # 일반 어린이
    'txtCompaCnt3': 0,  # 장애1-3 어른
    'txtCompaCnt4': 0,  # 장애1-3 어린이
    'txtCompaCnt5': 0,  # 경로 어른
    'txtCompaCnt6': 0,  # 청소년
    'txtCompaCnt7': 0,  # 장애4-6 어
    'txtJobId': '1101',  # 개인예약:'1101', 에약대기:'1102', SEATMAP예약:'1103'
    'txtJrnyCnt': '1',  # 여정 수
    'txtPsrmClCd1': 1,  # 일반실:1
    'txtJrnySqno1': '001',  # ?? 고정인듯
    'txtJrnyTpCd1': '11',  # 편도:11, 환승:14
    'txtDptDt1': year + month + day,  # 이렇게 하면 새벽기차는 날짜가 달라질텐데...
    'txtDptRsStnCd1': stations[depart_station],  # 출발역 코드
    'txtDptRsStnCdNm1': depart_station,  # 출발역 이름
    'txtDptTm1': '**',  # 출발시간
    'txtArvRsStnCd1': stations[arrive_station],  # 도착역 코드
    'txtArvRsStnCdNm1': arrive_station,  # 도착역 이름
    'txtArvTm1': '**',  # 도착시간
    'txtTrnNo1': '**',  # 열차 번호 (열차관련 정보)
    'txtRunDt1': year + month + day,  # 날짜
    'txtTrnClsfCd1': '00',  # ?? 고정인듯
    'txtTrnGpCd1': '100',  # 고정하면될듯..
    'txtChgFlg1': 'N',  # ?? 고정인듯
}


######################################################################
###########################    LOGICS    #############################
######################################################################


def login(id, pw):
    param = meta.make_login_param(id, pw)

    response = requests.post(meta.login_url, headers=meta.login_header, params=param)

    if '비밀번호 5회 오류시 로그인할 수 없습니다' in response.text:
        return False
    if 'ret_url' in response.text \
            and 'strWebPwdCphdAt' in response.text \
            and response.cookies['JSESSIONID']:
        cookies['JSESSIONID'] = response.cookies['JSESSIONID']
        return True


# <li class="log_nm">홍길동<span><b>님 환영합니다.</b></span><!-- <a href=javascript:goMem() tabindex="2" ></a> --></li>
# <li><a href="#" onclick="return m_logout_link()"><img src="/images/gnb_logout.gif" alt="로그아웃" /></a></li>
def login_confirm():
    response = requests.post(meta.login_confirm_url,
                             headers=meta.common_header,
                             cookies=cookies,
                             params=meta.login_confirm_param)

    if bs(response.text, 'html.parser').find('li', attrs={"class": "log_nm"}):
        return True
    else:
        return False


def find_empty_seats():
    print('\n좌석을 조회합니다..')
    response = requests.post(meta.lookup_url, headers=meta.common_header, cookies=cookies, params=lookup_param)

    # TODO: 나중에 열차 정보를 적절한 객체에 담자.
    tr_list = bs(response.text, 'html.parser').select('#tableResult > tr')
    for tr in tr_list:
        td_list = bs(str(tr), 'html.parser').select('td')
        # train_type = bs(str(td_list[1]), 'html.parser').find('span').text.strip()
        # if train_type != meta.KTX:
        #     continue

        depart_time = td_list[2].text.replace(depart_station, ' ').replace(':', '').strip()
        arrive_time = td_list[3].text.replace(arrive_station, ' ').replace(':', '').strip()

        train_number = bs(str(td_list[1]), 'html.parser').find('a').text.strip().rjust(5, '0')
        # first_class_seat = td_list[4]  # 필요하면 쓰도록
        economy_class_seat_info = td_list[5]
        # child_seat = td_list[6]

        print('train number : {}, depart_time:{}, arrive_time:{}'
              .format(train_number, depart_time, arrive_time))

        if not int(depart_time) < int(reserve_max_time):
            print('train number={}는 예약대상이 아닙니다.'.format(train_number))
            continue

        if can_reserve(economy_class_seat_info) and \
                reserve(depart_time, arrive_time,train_number.ljust(6, '0')):
            return True
    return False


def can_reserve(seat_info):
    return '예약하기' in str(seat_info)


def reserve(depart_time, arrive_time, train_number):
    print('[try to reserve] train number : {}, depart_time:{}, arrive_time:{}'
          .format(train_number, depart_time, arrive_time))

    header = dict(meta.common_header)
    header['Referer'] = 'http://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do'

    param = dict(reserve_param)
    param['txtTrnNo1'] = train_number
    param['txtDptTm1'] = depart_time.ljust(6, '0')
    param['txtArvTm1'] = arrive_time.ljust(6, '0')

    response = requests.post(meta.reserve_url, headers=meta.common_header, cookies=cookies, params=param)

    if response.status_code == 200 and meta.reserv_success_msg in response.text:
        print(meta.reserv_success_msg)
        return True
    elif meta.reserv_time_limit_msg in response.text:
        print(meta.reserv_time_limit_msg)
    return False


def validate_setting_info():
    if int(time.strftime('%Y%m%d')) > int(year + month + day):
        return False

    am_4 = int('0400')
    if am_4 < int(reserve_max_time) < int(reserve_min_time):
        return False

    if depart_station not in stations.keys() or arrive_station not in stations.keys():
        return False

    return True


def announce_success():
    mixer.init()
    mixer.music.load('gunshot.mp3')
    # wait for load
    time.sleep(1)
    # wait for load
    for i in range(1, 5):
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
    shutdown()

while True:
    try:
        result = find_empty_seats()
        if (result):
            print('---------예약성공---------')
            break
    except Exception as error: #가능하면 네트워크 과다요청 혹은 세션 문제일 때만 잡아내도록 바꾸자.
        print(error)
        login(id, pw)
    time.sleep(sleep_time)

announce_success()
