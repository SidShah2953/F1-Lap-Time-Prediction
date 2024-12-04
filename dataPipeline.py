import scripts.initialization
import scripts.dataCollection
import scripts.dataPreprocessing
import scripts.dataProcessing

if __name__ == "__main__":
    scripts.initialization.main()
    scripts.dataCollection.main()
    scripts.dataPreprocessing.main()
    scripts.dataProcessing.main()