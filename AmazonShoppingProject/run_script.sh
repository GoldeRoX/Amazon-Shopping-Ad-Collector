while true;
do

# Background start appium The service is used to listen for interface operations
appium &
sleep 10s
# Background start android Simulator
cd /home/krzysztof/android-sdk/emulator && ./emulator -avd Development -http-proxy http://151.236.15.140:3128 &
sleep 5s
# Run automated test cases in the background , And output the result to test_result.txt in
cd /home/krzysztof/PycharmProjects/AmazonShopping-AdCollector/AmazonShoppingProject && python3 main.py
done


