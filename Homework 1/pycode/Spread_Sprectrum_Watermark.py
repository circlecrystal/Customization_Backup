from math import sqrt, log10
from numpy import uint8, zeros, dot, copy as npcopy, array as nparray
from numpy.random import randn, shuffle
from os import makedirs, listdir, remove
from os.path import exists, isfile, join as pjoin
from PIL.Image import fromarray, open as iopen
from pylab import plot, xlabel, ylabel, savefig, figure
from scipy import sign
from scipy.fftpack import dct, idct
from shutil import rmtree

class Gaussian_Sequence(object):
    def __init__(self, re_gaus=False, seq_num=1, seq_len=223):
        gaus_dir = 'Watermark'
        if re_gaus==True or not exists(gaus_dir):
            self.gaus_gen(gaus_dir, seq_num, seq_len)
        self.x_array_array = self.x_gen(gaus_dir)

    def gaus_gen(self, gaus_dir, seq_num, seq_len):
        if exists(gaus_dir):
            rmtree(gaus_dir)
        try:
            makedirs(gaus_dir)
        except:
            print("Dir make failed on '%s'" %(gaus_dir))
        for i in range(1, seq_num+1):
            try:
                fout = open('%s/Gaussian%d.seq' %(gaus_dir, i), 'w')
                seq = [str(item) for item in list(randn(seq_len))]
                fout.write(' '.join(seq)+'\n')
                fout.close()
            except:
                print("File open failed on 'Gaussian%d.seq'" %(i))

    def x_gen(self, gaus_dir):
        x = []
        for name, path in self.seq_list_gen(gaus_dir):
            fin = open(path)
            x.append([sign(float(item)) for item in fin.read().split()])
            fin.close()
        return nparray(x, dtype=float)

    def seq_list_gen(self, gaus_dir):
        seq_list = []
        counter = 0
        for name in listdir(gaus_dir):
            path = pjoin(gaus_dir, name)
            if isfile(path) and name.endswith('.seq'):
                counter += 1
        for i in range(1, counter+1):
            name = 'Gaussian'+str(i)+'.seq'
            seq_list.append((name, pjoin(gaus_dir, name)))
        return seq_list


class Spread_Spectrum_Watermark(object):
    def __init__(self, image_name, image_dir):
        self.image = self.file_process(image_name, image_dir)
        image_array = nparray(self.image.convert('YCbCr'), dtype=float)
        Y_dcted_array, self.Cb_array, self.Cr_array = \
                                                self.image_dct(image_array)
        self.zz_order_list = self.zz_gen(image_array)
        self.v_array = self.v_gen(Y_dcted_array)

    def file_process(self, image_name, image_dir):
        image_path = pjoin(image_dir, image_name)
        try:
            return iopen(image_path)
        except:
            print("Image open failed on %s" %(image_path))

    def image_dct(self, image_array):
        dim = len(image_array)
        Y = npcopy(image_array).tolist()
        Cb = npcopy(image_array).tolist()
        Cr = npcopy(image_array).tolist()
        for i in range(dim):
            for j in range(dim):
                Y[i][j] = Y[i][j][0]
                Cb[i][j] = Cb[i][j][1]
                Cr[i][j] = Cr[i][j][2]
        Y = nparray(Y, dtype=float)
        Cb = nparray(Cb, dtype=float)
        Cr = nparray(Cr, dtype=float)
        Y_dcted = dct(dct(Y.T, norm='ortho').T, norm='ortho')
        return Y_dcted, Cb, Cr

    def zz_gen(self, image_array):
        dim = len(image_array)
        zz_order_list = []
        for i in range(1, dim):
            if i%2 == 1:
                row = i
                col = 1
                for j in range(i):
                    zz_order_list.append((row-j-1, col+j-1))
            else:
                row = 1
                col = i
                for j in range(i):
                    zz_order_list.append((row+j-1, col-j-1))
        for i in range(dim-1, 0, -1):
            if i%2 == 1:
                row = dim
                col = dim-i+1
                for j in range(i):
                    zz_order_list.append((row-j-1, col+j-1))
            else:
                row = dim-i+1
                col = dim
                for j in range(i):
                    zz_order_list.append((row+j-1, col-j-1))
        return zz_order_list

    def v_gen(self, Y_dcted_array):
        zz_order_list = self.zz_order_list
        v = []
        for j, k in zz_order_list:
            v.append(Y_dcted_array[j][k])
        return nparray(v, dtype=float)

    def ebd_ord_gen(
            self, 
            seq_len, 
            ord_dir='Embedding Order', 
            ord_name='Embedding_Order_List.txt', 
            re_ord=False):
        ord_path = pjoin(ord_dir, ord_name)
        if re_ord==True or not exists(ord_path):
            if exists(ord_dir):
                rmtree(ord_dir)
            try:
                makedirs(ord_dir)
            except:
                print("Dir make failed on '%s'" %(ord_dir))
            v = self.v_array.tolist()[1:]  # DC not included
            embedding_order = []
            temp = []
            for i, j in enumerate(v):
                temp.append((j, i))
            temp.sort()  # choose seq_len highest magnified components
            temp = temp[:seq_len]
            for i, j in temp:
                embedding_order.append(j+1)  # j+1 to exclude DC
            embedding_order = nparray(embedding_order)
            shuffle(embedding_order)
            self.embedding_order_list = embedding_order.tolist()
            try:
                fout = open(ord_path, 'w')
            except:
                print("File open for write failed on '%s'" %(ord_name))
            for i in self.embedding_order_list:
                fout.write('%s ' %(i))
            fout.close()
        else:
            try:
                fin = open(ord_path, 'r')
            except:
                print("File open for read failed on '%s'" %(ord_name))
            self.embedding_order_list = [int(i) for i in fin.read().split()]

    def embed_watermark(
            self, 
            output_path, 
            alpha, 
            embedding_order_list, x_array):
        seq_len = len(x_array)
        assert seq_len == len(embedding_order_list)
        v_list = self.v_array.tolist()
        x_list = x_array.tolist()
        for i in range(seq_len):
            v_list[embedding_order_list[i]] += alpha * x_list[i]
        dim = len(self.Cb_array)
        zz_order_list = self.zz_order_list
        Y_e = zeros((dim, dim)).tolist()
        for i in range(len(v_list)):
            row, col = zz_order_list[i]
            Y_e[row][col] = v_list[i]
        Y_e = nparray(Y_e, dtype=float)
        Y_e = idct(idct(Y_e.T, norm='ortho').T, norm='ortho')
        Y_e = Y_e.tolist()
        Cb = self.Cb_array.tolist()
        Cr = self.Cr_array.tolist()
        image_e = zeros((dim, dim, 3)).tolist()
        for i in range(dim):
            for j in range(dim):
                image_e[i][j] = round(Y_e[i][j]), Cb[i][j], Cr[i][j]
        image_e = fromarray(nparray(image_e, dtype=uint8), 'YCbCr').convert(
                                                    'RGB').save(output_path)

    def calc_similarity(self, x_array, embedding_order_list, v_array_new):
        v_array = self.v_array
        x_ex = []  # extracted x
        v_new_cropped = []
        for i in embedding_order_list:
            x_ex.append(sign(float(v_array_new[i] - v_array[i])))
            v_new_cropped.append(v_array_new[i])
        x_ex = nparray(x_ex)
        v_new_cropped = nparray(v_new_cropped)
        assert len(x_ex) == len(x_array)
        informed_similarity = dot(x_ex, x_array) / sqrt(dot(x_ex, x_ex))
        blind_similarity = dot(x_array, v_new_cropped) / sqrt(dot(
                                                v_new_cropped, v_new_cropped))
        return informed_similarity, blind_similarity

    def calc_psnr(self, image_name, image_dir):
        image = nparray(self.image, dtype=uint8).tolist()
        image_new = nparray(self.file_process(image_name, image_dir), dtype=
                                                                uint8).tolist()
        dim = len(image)
        MSE = 0
        for i in range(dim):
            for j in range(dim):
                for k in range(3):
                    MSE += (image[i][j][k]-image_new[i][j][k]) ** 2
        MSE = MSE/(3*dim*dim)
        return 10 * log10(255**2/MSE)


def user_interface(
        original_image_name='airplane.bmp', 
        embedded_image_name='embedded.bmp',
        test_image_name='embedded.bmp', 
        alpha=100,
        seq_len=223,
        mode=1):
    """mode: 1 for testing new image only(substitute test_image_name)"""
    """      2 for new embedding and overwrite everything            """
    gs_obj = Gaussian_Sequence(
            re_gaus=(mode==2), 
            seq_num=1, 
            seq_len=seq_len)
    ssw_obj = Spread_Spectrum_Watermark(
            image_name = original_image_name,
            image_dir = 'some_test_images')
    ssw_obj.ebd_ord_gen(
            seq_len=seq_len,
            ord_dir='Embedding Order', 
            ord_name='Embedding_Order_List.txt', 
            re_ord=(mode==2))
    if (mode==2)==True or not exists(embedded_image_name):
        ssw_obj.embed_watermark(
                output_path = embedded_image_name,
                alpha = alpha,
                embedding_order_list = ssw_obj.embedding_order_list,
                x_array = gs_obj.x_array_array[0])
    ssw_obj_test = Spread_Spectrum_Watermark(
            image_name = test_image_name,
            image_dir = '.')
    print(
            'PSNR:', 
            ssw_obj.calc_psnr(image_name = test_image_name,
            image_dir = '.'))
    original_embedding_order_list = ssw_obj.embedding_order_list
    informed_list = []
    blind_list = []
    for i in range(999):
        new_embedding_order = nparray(original_embedding_order_list)
        shuffle(new_embedding_order)
        new_embedding_order = new_embedding_order.tolist()
        if i == 200:
            inf_sim, bli_sim = ssw_obj.calc_similarity(
                    x_array = gs_obj.x_array_array[0], 
                    embedding_order_list = original_embedding_order_list,
                    v_array_new = ssw_obj_test.v_array)
        else:
            inf_sim, bli_sim = ssw_obj.calc_similarity(
                    x_array = gs_obj.x_array_array[0], 
                    embedding_order_list = new_embedding_order,
                    v_array_new = ssw_obj_test.v_array)
        informed_list.append(inf_sim)
        blind_list.append(bli_sim)
    if exists('Informed.png'):
        remove('Informed.png')
    if exists('Blind.png'):
        remove('Blind.png')
    a = figure()
    plot(informed_list)
    xlabel('Random Watermarks')
    ylabel('Watermark Detector Response')
    a.savefig('Informed.png')
    b = figure()
    plot(blind_list)
    xlabel('Random Watermarks')
    ylabel('Watermark Detector Response')
    b.savefig('Blind.png')


if __name__=='__main__':
    user_interface(
            original_image_name='fruits.bmp', 
            embedded_image_name='embedded.bmp',
            test_image_name='embedded.bmp', 
            alpha=100,
            seq_len=223,
            mode=1)
