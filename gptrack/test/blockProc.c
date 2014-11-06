#include <stdio.h>
#include <string.h>

#define POS(i, j, n, N, nch) ((i)*N*nch + (j)*nch + n)
#define POS1(i, j, N) (POS(i, j, 0, N, 1))
#define POS3(i, j, n, N) (POS(i, j, n, N, 3))


void compute(int*, int, int*, int, int);


/******/
int hist(int *in, int M1, int N1, int nch, int *out, int M2, int N2,
		 int w, int skip, int nbins)
{
	int i, j, y, x, n, a, b;
	int L = w*w*nch;
	int K = nch*nbins;
	int *tmp = (int*) malloc(sizeof(int) * L);
	int *bh = (int*) malloc(sizeof(int) * K);

	for (i=0, a=0; i<M1-w; i+=skip)
		for (j=0; j<N1-w; j+=skip) {

			for (y=0, b=0; y<w; y++)
				for (x=0; x<w; x++)
					for (n=0; n<nch; n++)
						tmp[b++] = in[POS3(i+y, j+x, n, N1)];

			memset(bh, 0, sizeof(int)*K);
			compute(tmp, L, bh, nch, nbins);

			for (y=0; y<K; y++) {
				out[POS1(a, y, N2)] = bh[y];
			}

			a++;
		}

	return 1;
}

/* --------------------------------------- */
void compute(int *tmp, int L, int *h, int nch, int nbins)
{
	int i, j, idx;
	int delta = 255/nbins;

	for (i=0; i<L-nch; ) {
		h[tmp[i++]/delta]++;
		h[tmp[i++]/delta + nbins]++;
		h[tmp[i++]/delta + 2*nbins]++;
	 }
	
}
