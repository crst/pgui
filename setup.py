from setuptools import setup, find_packages


def long_description():
    with open('README', 'r') as f:
        return f.read()


setup(name='pgui',
      version='1.0rc1',
      description='TBA',
      long_description=long_description(),
      author='Christopher Strecker',
      author_email='chris@foldl.de',
      url='https://github.com/crst/pgui',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'flask>=0.10.1',
          'flask-login>=0.2.11',
          'psycopg2>=2.6'
      ],
      license='MIT License'
)
