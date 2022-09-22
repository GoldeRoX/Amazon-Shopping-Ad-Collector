import subprocess
import shlex
import sys

from selenium.common.exceptions import InvalidSessionIdException

from AmazonShoppingProject.ads_logic import *
from AmazonShoppingProject.database_connector import get_random_keyword

from AmazonShoppingProject.base import *


def main(udid: int):
    pars = shlex.split(f"./emulator -avd Amazon-{udid} -http-proxy http://151.236.15.140:3128 -port {udid}")

    p = subprocess.Popen(pars, cwd="/home/krzysztof/android-sdk/emulator")
    time.sleep(10)
    start_time = time.time()

# TODO naprawic ten blad
    """
    Message: The session identified by 46ae0d83-4d9c-4083-86f9-02a125dca591 is not known
Stacktrace:
io.appium.uiautomator2.common.exceptions.NoSuchDriverException: The session identified by 46ae0d83-4d9c-4083-86f9-02a125dca591 is not known
	at io.appium.uiautomator2.handler.request.SafeRequestHandler.handle(SafeRequestHandler.java:54)
	at io.appium.uiautomator2.server.AppiumServlet.handleRequest(AppiumServlet.java:266)
	at io.appium.uiautomator2.server.AppiumServlet.handleHttpRequest(AppiumServlet.java:260)
	at io.appium.uiautomator2.http.ServerHandler.channelRead(ServerHandler.java:68)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:366)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:352)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:345)
	at io.netty.handler.codec.MessageToMessageDecoder.channelRead(MessageToMessageDecoder.java:102)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:366)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:352)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:345)
	at io.netty.channel.CombinedChannelDuplexHandler$DelegatingChannelHandlerContext.fireChannelRead(CombinedChannelDuplexHandler.java:435)
	at io.netty.handler.codec.ByteToMessageDecoder.fireChannelRead(ByteToMessageDecoder.java:293)
	at io.netty.handler.codec.ByteToMessageDecoder.channelRead(ByteToMessageDecoder.java:267)
	at io.netty.channel.CombinedChannelDuplexHandler.channelRead(CombinedChannelDuplexHandler.java:250)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:366)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:352)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:345)
	at io.netty.handler.timeout.IdleStateHandler.channelRead(IdleStateHandler.java:266)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:366)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:352)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:345)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.channelRead(DefaultChannelPipeline.java:1294)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:366)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:352)
	at io.netty.channel.DefaultChannelPipeline.fireChannelRead(DefaultChannelPipeline.java:911)
	at io.netty.channel.nio.AbstractNioByteChannel$NioByteUnsafe.read(AbstractNioByteChannel.java:131)
	at io.netty.channel.nio.NioEventLoop.processSelectedKey(NioEventLoop.java:611)
	at io.netty.channel.nio.NioEventLoop.processSelectedKeysOptimized(NioEventLoop.java:552)
	at io.netty.channel.nio.NioEventLoop.processSelectedKeys(NioEventLoop.java:466)
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:438)
	at io.netty.util.concurrent.SingleThreadEventExecutor$2.run(SingleThreadEventExecutor.java:140)
	at io.netty.util.concurrent.DefaultThreadFactory$DefaultRunnableDecorator.run(DefaultThreadFactory.java:144)
	at java.lang.Thread.run(Thread.java:764)
	"""

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
    except (WebDriverException, InvalidSessionIdException):
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)

    session.config_start()
    session.first_launch()
    session.change_lang_from_eng_to_de()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    keyword = get_random_keyword()
    keyword_id = keyword["id"]

    session.get_page(keyword["keyword"])

    try:

        """scroll down through app Y and collect ads"""
        is_end_of_page = False
        previous_page_source = session.driver.page_source

        while not is_end_of_page:
            session.cookies_click()
            ad_handler.collect_video_ad(session_id, keyword_id)
            # ad_handler.collect_ad_type_4(session_id, keyword_id)
            ad_handler.collect_ad_type_5(session_id, keyword_id)
            #TODO
            # naprawic problem z brakiem txt
            # ad_handler.collect_ad_type_1(session_id, keyword_id)

            session.scroll_down()

            is_end_of_page = previous_page_source == session.driver.page_source
            previous_page_source = session.driver.page_source

        # ad_handler.collect_ad_type_1(session_id, keyword_id)
        # ad_handler.collect_ad_type_2(session_id, keyword_id)
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        p.terminate()
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running ---" % (time.time() - start_time))
