def build_config():
    """
        vitalsign_mode: "breath" / "heart"
        Mode: single/multiple
        current_wiget: 　"0" / "1" / "2"
        save_type: bool -> excel / .npy (dict) / figure
        multi_dataset :  bool -> liedataset / seatdataset / aicadjust / sicadjust
        pw_targetidx :  bool -> phase map / max power
        pw_phaseprocess: bool ->  Raw unwrap phase / phase diff / cwt / vmd / phase coherence
        pw_HBCalc: bool ->   STFT / IBI

    """
    widget_cfg = {
        "vitalsign_mode": "",
        "current_wiget": "",
        "Mode": "single",
        "single_file_path": "",
        "save_result_path": "",
        "save_type": [False, False, False],
        "multi_dataset": [False, False, False, False],
        "pw_targetidx": [],
        "pw_phaseprocess": [],
        "pw_HBCalc": [],
        "vital_sign_window_len": 256,
        "vital_sign_shfit_len": 5,

    }
    return widget_cfg
