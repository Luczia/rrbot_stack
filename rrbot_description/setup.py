import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'rrbot_description'

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
        # Include model and simulation files
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lucas',
    maintainer_email='lucas.soubeyrand@gmail.com',
    description='ROS 2 description package for RRBot',
    license='',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #'state_publisher = rrbot_description.state_publisher:main'
        ],
    },
)
