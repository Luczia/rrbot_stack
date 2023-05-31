import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'rrbot_bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
     
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Luczia',
    maintainer_email='lucas.soubeyrand@gmail.com',
    description='ROS 2 bringup package for rrbot',
    license='',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #'state_publisher = rrbot_description.state_publisher:main'
        ],
    },
)
