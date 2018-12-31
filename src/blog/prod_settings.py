ALLOWED_HOSTS = []

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'read_default_file': [os.path.join(BASE_DIR, 'config/db_setting.cnf')],
    #     }
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vitaldocz_blog',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'vitaldocz',
        'PASSWORD': 'vitaldocz',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES'
        }
    }
}

#CREATE DATABASE IF NOT EXISTS [vitaldocz_blog];
#USE 'vitaldocz_blog';
