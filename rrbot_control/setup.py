import os
from glob import glob
from setuptools import setup
from setuptools import find_packages
package_name = 'rrbot_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        # Include model and simulation files
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='luczia',
    maintainer_email='lucas.soubeyrand@gmail.com',
    description='ROS rrbot control package',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'joint_animation_node = rrbot_control.joint_animation:main',             
                'cart_animation_node = rrbot_control.cart:main',      
        ],
    },
)
