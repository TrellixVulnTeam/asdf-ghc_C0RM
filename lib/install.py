def install(install_dir, version):
  return None

if __name__ == '__main__':
  install_dir = os.environ['ASDF_INSTALL_PATH']
  version = os.environ['ASDF_INSTALL_VERSION']
  install(install_dir, version)
