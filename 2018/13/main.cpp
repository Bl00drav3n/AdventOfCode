#define _CRT_SECURE_NO_WARNINGS
#include <assert.h>
#include <stdio.h>
#include <stdlib.H>

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define TEST_INPUT 0

#define MAXIMUM(a, b) (((a) > (b)) ? (a) : (b))

enum direction {
	EAST,
	SOUTH,
	WEST,
	NORTH,

	NUM_DIRECTIONS,
	INVALID_DIRECTION
};

enum turn {
	LEFT,
	STRAIGHT,
	RIGHT,
};

const char * facing_to_cstr(direction d) {
	switch (d) {
	case EAST: return "east"; break;
	case SOUTH: return "south"; break;
	case WEST: return "west"; break;
	case NORTH: return "north"; break;
	}

	assert(0);
	return 0;
}

direction char_to_direction(char c) {
	switch (c) {
	case '>': return EAST;
	case 'v': return SOUTH;
	case '<': return WEST;
	case '^': return NORTH;
	}
	assert(0);
	return INVALID_DIRECTION;
}

char facing_to_char(direction facing) {
	switch (facing) {
	case EAST: return '>';
	case SOUTH: return 'v';
	case WEST: return '<';
	case NORTH: return '^';
	}
	assert(0);
	return 0;
}

struct cart {
	int id;
	int pos_x;
	int pos_y;
	direction facing;
	turn t;
};

int partition(cart * carts, int ncarts, int width, int lo, int hi) {
	cart * pivot = carts + (lo + hi) / 2;
	int pivot_value = pivot->pos_y * width + pivot->pos_x;
	int i = lo - 1;
	int j = hi + 1;
	for (;;) {
		do {
			i++;
		} while (width * carts[i].pos_y + carts[i].pos_x < pivot_value);
		do {
			j--;
		} while (width * carts[j].pos_y + carts[j].pos_x > pivot_value);

		if (i >= j)
			return j;

		cart tmp = carts[i];
		carts[i] = carts[j];
		carts[j] = tmp;
	}
}

void sort(cart * carts, int ncarts, int width, int lo, int hi) {
	if (lo < hi) {
		int p = partition(carts, ncarts, width, lo, hi);
		sort(carts, ncarts, width, lo, p);
		sort(carts, ncarts, width, p + 1, hi);
	}
}

struct state {
	char * tiles;
	int width;
	int height;

	int ncarts;
	cart * carts;

	int t;
};

void print_track(state * s) {
	for (int i = 0; i < s->ncarts; i++) {
		fprintf(stdout, "cart[%d] at %d,%d facing %s\n", s->carts[i].id, s->carts[i].pos_x, s->carts[i].pos_y, facing_to_cstr(s->carts[i].facing));
	}
	for (int y = 0; y < s->height; y++) {
		for (int x = 0; x < s->width; x++) {
			bool collision = false;
			bool found = false;
			direction facing = INVALID_DIRECTION;
			for (int i = 0; i < s->ncarts; i++) {
				if (s->carts[i].pos_x == x && s->carts[i].pos_y == y) {
					if (found) {
						collision = true;
					}
					else {
						found = true;
						facing = s->carts[i].facing;
					}
				}
			}
			char c = s->tiles[y * s->width + x];
			if (collision) c = 'X';
			else if (found) c = facing_to_char(facing);
			fputc(c, stdout);
		}
		fputc('\n', stdout);
	}
	fputc('\n', stdout);
}

void remove_cart(state * s, int idx) {
	if (idx >= 0 && idx < s->ncarts) {
		s->ncarts--;
		for (int i = idx; i < s->ncarts; i++) {
			s->carts[i] = s->carts[i + 1];
		}
	}
	else {
		assert(0);
	}
}

bool update(state * s) {
	bool collision = false;
	sort(s->carts, s->ncarts, s->width, 0, s->ncarts - 1);
	for (int i = 0; i < s->ncarts; i++) {
		cart * crt = s->carts + i;
		int x = crt->pos_x;
		int y = crt->pos_y;
		switch (crt->facing) {
		case EAST: x++; break;
		case SOUTH: y++; break;
		case WEST: x--; break;
		case NORTH: y--; break;
		default: assert(0);
		}
		crt->pos_x = x;
		crt->pos_y = y;
		char c = s->tiles[y * s->width + x];
		if (c == '+') {
			if (crt->t != STRAIGHT) {
				if (crt->facing == EAST) {
					crt->facing = (crt->t == LEFT) ? NORTH : SOUTH;
				}
				else if (crt->facing == SOUTH) {
					crt->facing = (crt->t == LEFT) ? EAST : WEST;
				}
				else if (crt->facing == WEST) {
					crt->facing = (crt->t == LEFT) ? SOUTH : NORTH;
				}
				else if (crt->facing == NORTH) {
					crt->facing = (crt->t == LEFT) ? WEST : EAST;
				}
			}
			crt->t = (turn)((crt->t + 1) % 3);
		}
		else if (c == '/') {
			if (crt->facing == EAST) {
				crt->facing = NORTH;
			}
			else if (crt->facing == SOUTH) {
				crt->facing = WEST;
			}
			else if (crt->facing == WEST) {
				crt->facing = SOUTH;
			}
			else if (crt->facing == NORTH) {
				crt->facing = EAST;
			}
		}
		else if (c == '\\') {
			if (crt->facing == EAST) {
				crt->facing = SOUTH;
			}
			else if (crt->facing == SOUTH) {
				crt->facing = EAST;
			}
			else if (crt->facing == WEST) {
				crt->facing = NORTH;
			}
			else if (crt->facing == NORTH) {
				crt->facing = WEST;
			}
		}

		// NOTE: Collision check
		for (int j = 0; j < s->ncarts; j++) {
			if (i == j)
				continue;
			cart * other = s->carts + j;
			if (crt->pos_x == other->pos_x && crt->pos_y == other->pos_y) {
				// NOTE: i and j collided, remove
				fprintf(stdout, "Collision after %d updates at position %d,%d\n", s->t, crt->pos_x, crt->pos_y);
				if (i < j) {
					remove_cart(s, j);
					remove_cart(s, i);
				}
				else {
					remove_cart(s, i);
					remove_cart(s, j);
					i--;
				}
				i--;
				collision = true;
				break;
			}
		}
	}
	return collision;
}

int main(int argc, char *argv[]) {
	LARGE_INTEGER Start, End, Freq;
#if TEST_INPUT
	const char * filename = "testinput.txt";
#else
	const char * filename = "input.txt";
#endif
	FILE *f = fopen(filename, "r");
	if (f) {
		char c;
		int x, y, width, height, cartid;
		int ncarts;

		direction facings[NUM_DIRECTIONS] = { EAST, SOUTH, WEST, NORTH };
		cart * carts = 0;
		char * tiles = 0;

		ncarts = 0;
		width = 0;
		height = 0;
		x = 0;
		do {
			c = fgetc(f);
			switch (c) {
			case '>': case '<': case 'v': case '^':
				ncarts++;
				break;
			case '\n':
				height++;
				width = MAXIMUM(width, x);
				x = 0;
				break;
			default:
				x++;
			}
		} while (c != EOF);

		tiles = (char*)malloc(width * height);
		carts = (cart*)malloc(ncarts * sizeof(cart));

		fseek(f, 0L, SEEK_SET);
		x = y = cartid = 0;
		do {

			c = fgetc(f);
			if (c == '\n') {
				x = 0;
				y++;
			}
			else {
				if (c == '>' || c == 'v' || c == '<' || c == '^') {
					cart * crt = carts + cartid;
					crt->id = cartid++;
					crt->pos_x = x;
					crt->pos_y = y;
					crt->facing = facings[char_to_direction(c)];
					crt->t = LEFT;
					if (c == '>' || c == '<')
						c = '-';
					else if (c == '^' || c == 'v')
						c = '|';
				}
				tiles[y * width + x] = c;
				x++;
			}
		} while (c != EOF);
		fclose(f);

		QueryPerformanceCounter(&Start);
		state s = {};
		s.tiles = tiles;
		s.height = height;
		s.width = width;
		s.carts = carts;
		s.ncarts = ncarts;
		s.t = 0;
#if TEST_INPUT
		print_track(&s);
#endif
		for (;;) {
			s.t++;
			bool collision;
			collision = update(&s);
			if (collision) {
#if TEST_INPUT
				print_track(&s);
#endif
				if (s.ncarts == 1) {
					fprintf(stdout, "remaining; cart[%d] at %d,%d\n", s.carts[0].id, s.carts[0].pos_x, s.carts[0].pos_y);
					break;
				}
				else if (s.ncarts == 0) {
					fprintf(stdout, "no carts remaining, terminating...\n");
					break;
				}
			}
		}
	}
	QueryPerformanceCounter(&End);
	QueryPerformanceFrequency(&Freq);

	LONGLONG Diff = End.QuadPart - Start.QuadPart;
	fprintf(stdout, "\n--- Timing: %.3fms ---\n", 1000.f * (float)Diff / (float)Freq.QuadPart);

	return 0;
}