from copy import copy
from math import sqrt, log10
from numpy import uint8, zeros, dot, copy as npcopy, array as nparray
from numpy.random import randn
from os import makedirs, listdir, remove
from os.path import exists, isfile, join as pjoin
from PIL.Image import fromarray, open as iopen
from pylab import plot, xlabel, ylabel, savefig, figure
from random import shuffle
from scipy import sign
from scipy.fftpack import dct, idct
from shutil import rmtree

EMBEDDING_PROCESS = 2  # 1 for v+=a*x, 2 for v*=1+a*x

class Gaussian_Sequence(object):
    def __init__(self, re_gaus=False, seq_num=1, seq_len=223):
        gaus_dir = 'Watermark'
        if re_gaus==True or not exists(gaus_dir):
            self.gaus_gen(gaus_dir, seq_num, seq_len)
        self.x_array_array = self.x_gen(gaus_dir)

    def gaus_gen(self, gaus_dir, seq_num, seq_len):
        try:
            rmtree(gaus_dir)
        except:
            pass
        try:
            makedirs(gaus_dir)
        except:
            pass
        for i in range(1, seq_num+1):
            try:
                fout = open('%s/Gaussian%d.seq' %(gaus_dir, i), 'w')
            except:
                print("File open failed on 'Gaussian%d.seq'" %(i))
            seq = [str(item) for item in list(randn(seq_len))]
            fout.write(' '.join(seq)+'\n')
            fout.close()

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
        self.zz_order_list = self.zz_ord(image_array)
        self.zz_array = self.zz_gen(Y_dcted_array)

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

    def zz_ord(self, image_array):
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

    def zz_gen(self, Y_dcted_array):
        zz_order_list = self.zz_order_list
        zz = []
        for j, k in zz_order_list:
            zz.append(Y_dcted_array[j][k])
        return nparray(zz, dtype=float)

    def v_ord(self, seq_len):
        zz = self.zz_array.tolist()[1:]  # DC not included
        v_ord = []
        zz_enu = []
        for i, j in enumerate(zz):
            zz_enu.append((j, i))
        zz_enu.sort()  # choose seq_len highest magnified components
        zz_enu = zz_enu[:seq_len]
        for i, j in zz_enu:
            v_ord.append(j+1)  # j+1 for excluded DC
        return v_ord

    def embed_ord_gen(
            self, 
            v_ord,
            ord_dir, 
            ord_name, 
            re_ord=False):
        ord_path = pjoin(ord_dir, ord_name)
        if re_ord==True or not exists(ord_path):
            try:
                makedirs(ord_dir)
            except:
                pass
            try:
                remove(ord_path)
            except:
                pass
            try:
                fout = open(ord_path, 'w')
            except:
                print("File open for write failed on '%s'" %(ord_name))
            embed_ord = copy(v_ord)
            shuffle(embed_ord)
            for i in embed_ord:
                fout.write('%s ' %(i))
            fout.close()

    def get_embed_ord(
            self,
            ord_dir,
            ord_name):
        ord_path = pjoin(ord_dir, ord_name)
        try:
            fin = open(ord_path, 'r')
        except:
            print("File open for read failed on '%s'" %(ord_name))
        return [int(i) for i in fin.read().split()]

    def embed_watermark(
            self, 
            alpha, 
            embed_ord, 
            x_array,
            zz_array):
        global EMBEDDING_PROCESS
        seq_len = len(x_array)
        assert seq_len == len(embed_ord)
        zz = zz_array.tolist()
        x_list = x_array.tolist()
        for i in range(seq_len):
            if EMBEDDING_PROCESS == 1:
                zz[embed_ord[i]] += alpha * x_list[i]
            else:
                zz[embed_ord[i]] *= 1 + alpha*x_list[i]
        return nparray(zz, dtype=float)

    def idct_out(
            self, 
            output_image_name, 
            output_dir,
            zz_array):
        zz = zz_array.tolist()
        dim = len(self.Cb_array)
        zz_order_list = self.zz_order_list
        Y_e = zeros((dim, dim)).tolist()
        for i in range(len(zz)):
            row, col = zz_order_list[i]
            Y_e[row][col] = zz[i]
        Y_e = nparray(Y_e, dtype=float)
        Y_e = idct(idct(Y_e.T, norm='ortho').T, norm='ortho')
        Y_e = Y_e.tolist()
        Cb = self.Cb_array.tolist()
        Cr = self.Cr_array.tolist()
        image_e = zeros((dim, dim, 3)).tolist()
        for i in range(dim):
            for j in range(dim):
                image_e[i][j] = round(Y_e[i][j]), Cb[i][j], Cr[i][j]
        fromarray(nparray(image_e, dtype=uint8), 'YCbCr').convert('RGB').save(
                                        pjoin(output_dir, output_image_name))

    def calc_similarity(self, x_array, embed_ord, zz_array_new, alpha):
        global EMBEDDING_PROCESS
        zz = self.zz_array.tolist()
        zz_new = zz_array_new.tolist()
        x_ex = []  # extracted x
        v_new_cropped = []
        for i in embed_ord:
            if EMBEDDING_PROCESS == 1:
                x_ex.append(round((zz_new[i] - zz[i])/alpha))
            else:
                x_ex.append(round((zz_new[i]/zz[i]-1)/alpha))
            v_new_cropped.append(zz_new[i])
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
        seq_num=5,
        mode=1):
    """mode: 1 for testing new image only(substitute test_image_name)"""
    """      2 for new embedding and overwrite everything            """
    gs = Gaussian_Sequence(
            re_gaus=(mode==2), 
            seq_num=seq_num, 
            seq_len=seq_len)
    ssw = Spread_Spectrum_Watermark(
            image_name=original_image_name,
            image_dir='some_test_images')
    if mode == 2:
        v_ord = ssw.v_ord(seq_len)
        try:
            rmtree('Embedding Order')
        except:
            pass
        for i in range(seq_num):
            ssw.embed_ord_gen(
                    v_ord,
                    ord_dir='Embedding Order', 
                    ord_name='Embedding_Order_List_%d.txt' %(i+1), 
                    re_ord=(mode==2))
            embed_ord = ssw.get_embed_ord(
                    ord_dir='Embedding Order',
                    ord_name='Embedding_Order_List_%d.txt' %(i+1))
            if i == 0:
                zz_array_embedded = ssw.embed_watermark(
                        alpha=alpha,
                        embed_ord=embed_ord,
                        x_array=gs.x_array_array[i],
                        zz_array=ssw.zz_array)
            else:
                zz_array_embedded = ssw.embed_watermark(
                        alpha=alpha,
                        embed_ord=embed_ord,
                        x_array=gs.x_array_array[i],
                        zz_array=zz_array_embedded)
        ssw.idct_out(
                output_image_name=embedded_image_name,
                output_dir='.',
                zz_array=zz_array_embedded)
    else:
        ssw_t = Spread_Spectrum_Watermark(
                image_name=test_image_name,
                image_dir='.')
        print(
                'PSNR:', 
                ssw.calc_psnr(
                    image_name=test_image_name,
                    image_dir='.'))
        if seq_num == 1:
            embed_ord = ssw.get_embed_ord(
                    ord_dir='Embedding Order',
                    ord_name='Embedding_Order_List_%d.txt' %(1))
            informed_list = []
            blind_list = []
            for i in range(999):
                new_embed_ord = copy(embed_ord)
                shuffle(new_embed_ord)
                if i == 200:
                    inf_sim, bli_sim = ssw.calc_similarity(
                            x_array=gs.x_array_array[0], 
                            embed_ord=embed_ord,
                            zz_array_new=ssw_t.zz_array,
                            alpha=alpha)
                    print('Informed Detect Similarity:', inf_sim)
                    print('Blind Detect Similarity:', bli_sim)
                else:
                    inf_sim, bli_sim = ssw.calc_similarity(
                            x_array=gs.x_array_array[0], 
                            embed_ord=new_embed_ord,
                            zz_array_new=ssw_t.zz_array,
                            alpha=alpha)
                informed_list.append(inf_sim)
                blind_list.append(bli_sim)
            try:
                remove('Informed.png')
            except:
                pass
            try:
                remove('Blind.png')
            except:
                pass
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
        else:
            print('Informed Similarity', end='\t')
            print('Blind Similarity', end='\t')
            print('Delta')
            for i in range(seq_num):
                embed_ord = ssw.get_embed_ord(
                        ord_dir='Embedding Order',
                        ord_name='Embedding_Order_List_%d.txt' %(i+1))
                inf_sim, bli_sim = ssw.calc_similarity(
                        x_array=gs.x_array_array[i], 
                        embed_ord=embed_ord,
                        zz_array_new=ssw_t.zz_array,
                        alpha=alpha)
                print('%.3f' %(inf_sim), end='\t\t\t')
                print('%.3f' %(bli_sim), end='\t\t\t')
                print('%.3f' %(inf_sim-bli_sim))


if __name__=='__main__':
    user_interface(
            original_image_name='airplane.bmp', 
            embedded_image_name='embedded.bmp',
            test_image_name='embedded.bmp', 
            alpha=0.05,
            seq_len=223,
            seq_num=100,
            mode=1)
