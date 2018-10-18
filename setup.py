from setuptools import setup, find_packages

setup(
      name = 'jokes_api',
      version = '1.0.0',
      license='MIT',
      packages=['flask_app'],
      author = 'Yuliya Chernobay',
      author_email = 'jamsic@yandex.ru',
      description = 'API for jokes',
      install_requires=['Click==7.0', 'Flask==1.0.2',
                        'Flask-HTTPAuth==3.2.4', 'Flask-RESTful==0.3.6',
                        'Flask-SQLAlchemy==2.3.2', 'Jinja2==2.10',
                        'MarkupSafe==1.0', 'SQLAlchemy==1.2.12',
                        'Werkzeug==0.14.1', 'aniso8601==3.0.2',
                        'asn1crypto==0.24.0', 'certifi==2018.10.15',
                        'cffi==1.11.5', 'chardet==3.0.4', 'idna==2.7',
                        'cryptography==2.3.1', 'itsdangerous==0.24', 
                        'pyOpenSSL==18.0.0', 'pycparser==2.19', 
                        'pytz==2018.5', 'requests==2.19.1', 'six==1.11.0',
                        'urllib3==1.23', 'wsgiref==0.1.2',],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 3 - Alpha',
      ],
    )

