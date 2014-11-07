#include <stdio.h>
#include <string.h>

#define POS(i, j, n, N, nch) ((i)*N*nch + (j)*nch + n)
#define POS1(i, j, N) (POS(i, j, 0, N, 1))
#define POS3(i, j, n, N) (POS(i, j, n, N, 3))

#define INTZEROS(ptr, K) memset(ptr, 0, sizeof(int)*K)
#define FLOATZEROS(ptr, K) memset(ptr, 0, sizeof(float)*K)

#define PIXEL_LOOP(M, N, w, s) \
	for (i=0, a=0; i<M-w; i+=s)	\
		for (j=0; j<N-w; j+=s)

#define PATCH_LOOP(w, nch) \
	for (y=0, b=0; y<w; y++) \
		for (x=0; x<w; x++) \
			for (n=0; n<nch; n++)

#define OUT_LOOP(K) \
	for (y=0; y<K; y++)


void compute_hist(int*, int, int*, int, int);
void compute_grad(float*, int, float*);


int hist(int *in, int M1, int N1, int nch, int *out, int M2, int N2,
		 int w, int skip, int nbins)
{
	int i, j, y, x, n, a, b;
	int L = w*w*nch;
	int K = nch*nbins;
	int *block = (int*) malloc(sizeof(int) * L);
	int *bh = (int*) malloc(sizeof(int) * K);

	PIXEL_LOOP(M1, N1, w, skip) {
		PATCH_LOOP(w, nch) {
			block[b++] = in[POS3(i+y, j+x, n, N1)];
		}

		INTZEROS(bh, K);
		compute_hist(block, L, bh, nch, nbins);

		OUT_LOOP(K) {
			out[POS1(a, y, N2)] = bh[y];
		}

		a++;
	}

	return 1;
}
 
void compute_hist(int *tmp, int L, int *h, int nch, int nbins)
{
	int i, j;
	int delta = 255/nbins;

	for (i=0; i<L-nch; ) {
		h[tmp[i++]/delta]++;
		h[tmp[i++]/delta + nbins]++;
		h[tmp[i++]/delta + 2*nbins]++;
	 }
}


int gradient(float *in, int M1, int N1, int nch, float *out, int M2, int N2,
			 int w, int skip)
{
	int i, j, y, x, a, b, n;
	int L = w*w*nch;
	int K = nch;
	float *block = (float*) malloc(sizeof(float) * L);
	float *sum = (float*) malloc(sizeof(float) * K);

	PIXEL_LOOP(M1, N1, w, skip) {
		PATCH_LOOP(w, nch) {
			block[b++] = in[POS3(i+y, j+x, n, N1)];
		}
				
		FLOATZEROS(sum);
		compute_grad(block, L, sum);
				
		OUT_LOOP(K) {
			out[POS1(a, y, N2)] = sum[y];
		}

		a++;
	}

	return 1;
}

void compute_grad(int *block, int L, float *sum)
{
	int i;

	for (i=0; i<L; i++) {
		sum[i % 3] += block[i];
	}
}


