import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'rrbot_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('scripts', package_name, 'scripts'), glob('scripts/*')),        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='luczia',
    maintainer_email='lucas.soubeyrand@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'entity_spawner = rrbot_gazebo.entity_spawner:main',
        ],
    },
)
