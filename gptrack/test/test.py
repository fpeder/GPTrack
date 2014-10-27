from classifier import SkinClassifier

if __name__ == '__main__':
    import sys
    import cv2

    sc = SkinClassifier()
    sc.load('model/asd.pkl')
    sc.predicit(cv2.imread(sys.argv[1]))
