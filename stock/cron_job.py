from crontab import CronTab

cron = CronTab(user=True)

# Tạo một cron job mới
job = cron.new(command= 'python stock/main.py')

# Thiết lập chạy hàng ngày lúc 6:00 sáng
job.setall('0 6 * * *')

# Lưu cron job
cron.write()

print("Cron job đã được thêm!")
