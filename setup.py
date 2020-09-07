import setuptools
from pip._internal import req


setuptools.setup(
    name='sizex',
    version='0.0.1',
    author='Henry Pro',
    author_email='henry@sl-team.ru',
    description='',
    zip_safe=False,
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[str(ir.req) for ir in req.parse_requirements('requirements.txt', session='hack')]
)
