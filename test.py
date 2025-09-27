import asyncio
import time


async def send_mail(num):
    print('Улетело сообщение {}'.format(num))
    await asyncio.sleep(1)
    print('Сообщение {} доставлено'.format(num))


async def main():
    tasks = [send_mail(i) for i in range(10)]
    await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
print(f'Время выполнения программы: {time.time() - start_time} с')