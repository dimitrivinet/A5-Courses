import modules.models
import modules.train

N_CLASSES = 10
DATASET_DIR = "/home/dimitri/Documents/A5-Courses/AI/AI01/dataset"
SAVE_PATH = "/home/dimitri/Documents/A5-Courses/AI/AI01/output"
NUM_EPOCHS = 100
SAVE_ALL=False

def main():
    model = modules.models.MLP(N_CLASSES)
    # model = modules.models.LeNet5(N_CLASSES)
    # model = modules.models.VGG16(N_CLASSES)
    # model = modules.models.ResNet15(N_CLASSES)


    modules.train.train(model=model,
        dataset_dir=DATASET_DIR,
        save_path=SAVE_PATH,
        num_epochs=NUM_EPOCHS,
        save_all=SAVE_ALL)

if __name__ == "__main__":
    main()
