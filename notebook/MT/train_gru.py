# Hyperparameter configuration
HYPERPARAMETERS = {
    # Data paths
    'data_path': './data/splits/',  # Base directory for all data files
    'train_path': './data/splits/es_train.csv',
    'val_path': './data/splits/es_val.csv',
    'test_path': './data/splits/es_test.csv',
    'output_dir': './models',
    
    # Model parameters
    'vocab_size': 10000,
    'embedding_dim': 256,
    'units': 1024,
    'batch_size': 64,
    
    # Training parameters
    'epochs': 50,
    'learning_rate': 0.001,
    'clip': 1.0,
    'teacher_forcing_ratio': 0.5,
    'save_every': 5,
    'seed': 42,
    'no_cuda': False,
    
    # Optional parameters
    'dropout': 0.1,
    'early_stopping_patience': 5,
    'scheduler_factor': 0.1,
    'scheduler_patience': 2,
    'warmup_epochs': 2
} 