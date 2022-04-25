ads_meta_data = []


for i in range(5):
    ads_meta_data.append([f"filename{i}", f"width{i}", f"height{i}", f"location_x{i}", f"location_y{i}", f"text{i}", f"timestamp{i}"])

for ad in ads_meta_data:
    try:
        print("bottom_ad", ad[0], ad[1], ad[2], ad[3],
                                       ad[4], ad[5], ad[6])
    except Exception as e:
        print(f'Excepion occured in sending meta_data to DB: {e}')
        pass