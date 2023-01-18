def get_model_dir_name(model_name):
    model_dir_name = model_name.replace(' ', '_')
    model_dir_name = model_dir_name.replace('.', '_')
    return model_dir_name
