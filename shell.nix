with import <nixpkgs> { };

pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = with python39Packages; [
    python
    venvShellHook
    numpy
    pillow
    scikitimage
    opencv4
    tkinter
  ];

  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -e .
  '';
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';
}
