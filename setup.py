from setuptools import setup, find_packages

install_requires = [
    'requests==2.31.0',
    'pytz==2019.1',
    'python-dateutil==2.8.0',
]

setup(
    name='qiwi_payments',
    version='0.1',
    packages=['qiwi_payments'],
    url='https://github.com/adilkhash/qiwi',
    license='MIT',
    author='Adylzhan Khashtamov',
    author_email='adil.khashtamov@gmail.com',
    description='Qiwi API client',
    install_requires=install_requires,
)
