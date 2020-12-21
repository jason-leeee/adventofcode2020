import os
import sys
import math
import copy
import itertools
import pickle
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def split_list(lines):
    lseps = []
    lsep = []
    for line in lines:
        if line:
            lsep.append(line)
        else:
            lseps.append(lsep)
            lsep = []
    lseps.append(lsep)
    return lseps


class Tile():
    def __init__(self, tile_id, tile_number, tile_size, tile_mat, tile_trans):
        self.tile_id = tile_id
        self.tile_id_full = str(tile_id) + "_" + str(self.trans_text_to_int(tile_trans))
        self.tile_number = tile_number
        self.tile_size = tile_size
        self.tile_mat = tile_mat
        self.tile_trans = tile_trans

        self.edge_left = self.make_vector_number(self.tile_mat[:, 0])
        self.edge_top = self.make_vector_number(self.tile_mat[0, :])
        self.edge_right = self.make_vector_number(self.tile_mat[:, -1])
        self.edge_bottom = self.make_vector_number(self.tile_mat[-1, :])
        
    def trans_text_to_int(self, trans):
        transmap = {
            "R90": 0, "R90H": 1, "R90V": 2, "R90HV": 12,
            "R180": 3, "R180H": 4, "R180V": 5, "R180HV": 13,
            "R270": 6, "R270H": 7, "R270V": 8, "R270HV": 14,
            "R360": 9, "R360H": 10, "R360V": 11, "R360HV": 15
        }
        return transmap[trans]

    def make_vector_number(self, vec):
        return int("".join(map(str, vec)))

    def print_mat(self):
        print(self.tile_mat)

    def print_edges(self):
        print(f"edge_left: {self.edge_left}")
        print(f"edge_top: {self.edge_top}")
        print(f"edge_right: {self.edge_right}")
        print(f"edge_bottom: {self.edge_bottom}")


def init_tiles(lines):
    tile_infos = split_list(lines)
    tiles = {}
    tiles_number = {}
    for tile_id, tile_info in enumerate(tile_infos):
        tile_number = int(tile_info[0].split(" ")[1][:-1])
        tile_info = tile_info[1:]
        tile_size = len(tile_info[0])
        tile_basic_info = (tile_id, tile_number, tile_size)

        tiles_number[tile_id] = tile_number

        # create the original matrix
        tile_mat = np.zeros((tile_size, tile_size), dtype=np.uint8)
        for y, row in enumerate(tile_info):
            for x, ch in enumerate(row):
                tile_mat[y][x] = 1 if ch == "." else 2
        #print(f"tile_id: {tile_id}\ntile_mat raw: \n{tile_mat}")

        # anti-clockwise rotate 90 degrees 4 times
        for degree in range(90, 361, 90):
            tile_mat = np.copy(np.rot90(tile_mat))
            tile = Tile(*tile_basic_info, tile_mat, f"R{degree}")
            tiles[tile.tile_id_full] = tile
            #print(f"tile_mat rotate {degree}: \n{tile_mat}")

            tile_mat_hflip = np.copy(np.fliplr(tile_mat))
            tile = Tile(*tile_basic_info, tile_mat_hflip, f"R{degree}H")
            tiles[tile.tile_id_full] = tile
            #print(f"tile_mat rotate {degree} hflip: \n{tile_mat_hflip}")
        #print("\n")
    
    #print(tiles.keys())
    print(f"init number of tiles: {len(tiles.keys())}")

    #tile_0_0 = tiles["3_7"]
    #tile_0_0.print_mat()
    #tile_0_0.print_edges()

    return tiles, tiles_number


class Block:
    def __init__(self, block_id, block_size):
        self.block_id = block_id
        self.block_size = block_size

    def init_from_tile(self, tile):
        self.block_mat = tile.tile_mat
        self.tile_arrange = np.array([[tile.tile_id]], dtype=np.int32)
        self.edge_left = tile.edge_left
        self.edge_top = tile.edge_top
        self.edge_right = tile.edge_right
        self.edge_bottom = tile.edge_bottom
        self.exist_tile_ids = {tile.tile_id: True}

    def init_from_subblocks(self, subblocks):
        #tile_size = subblocks[0].block_mat.shape[0] // subblocks[0].block_size
        #mat_size = self.block_size * tile_size
        mat_step = subblocks[0].block_mat.shape[0]
        mat_size = mat_step * self.block_size
        tile_arrange_step = subblocks[0].tile_arrange.shape[0]
        tile_arrange_size = tile_arrange_step * self.block_size
        self.block_mat = np.zeros((mat_size, mat_size), dtype=np.uint8)
        self.tile_arrange = np.zeros((tile_arrange_size, tile_arrange_size), dtype=np.int32)
        for i, subblock in enumerate(subblocks):
            row = i // self.block_size
            col = i % self.block_size
            # TODO: double check this?
            self.block_mat[row * mat_step: (row + 1) * mat_step, col * mat_step: (col + 1) * mat_step] = subblock.block_mat
            self.tile_arrange[row * tile_arrange_step: (row + 1) * tile_arrange_step, col * tile_arrange_step: (col + 1) * tile_arrange_step] = subblock.tile_arrange   # FIXME
        self.edge_left = self.make_vector_number(self.block_mat[:, 0])
        self.edge_top = self.make_vector_number(self.block_mat[0, :])
        self.edge_right = self.make_vector_number(self.block_mat[:, -1])
        self.edge_bottom = self.make_vector_number(self.block_mat[-1, :])
        self.exist_tile_ids = {}
        for subblock in subblocks:
            for k in subblock.exist_tile_ids.keys():   # TODO: optimize?
                self.exist_tile_ids[k] = True

    def make_vector_number(self, vec):
        return int("".join(map(str, vec)))

    def contain_tile_ids(self, ids):
        for v in ids:
            if v in self.exist_tile_ids:
                return True
        return False

    def print_mat(self):
        print(self.block_mat)

    def print_edges(self):
        print(f"edge_left: {self.edge_left}")
        print(f"edge_top: {self.edge_top}")
        print(f"edge_right: {self.edge_right}")
        print(f"edge_bottom: {self.edge_bottom}")

    def print_tiles(self):
        print(self.tile_arrange)


def block_search(depth, mat, block_size, subblocks, newblocks):
    if depth == block_size * block_size:
        #print(mat)
        newblock_id = len(newblocks)
        newblock = Block(block_id=newblock_id, block_size=block_size)
        mat_subblocks = [subblocks[block_id] for block_id in mat.flatten()]
        newblock.init_from_subblocks(mat_subblocks)
        newblocks[newblock_id] = newblock
        return

    row = depth // block_size
    col = depth % block_size
    for i, (subblock_id, subblock) in enumerate(subblocks.items()):
        #if depth == 0:
        #    print(f"[{i}] depth 0")

        if row > 0:
            subblock_top = subblocks[mat[row - 1][col]]
            if subblock.edge_top != subblock_top.edge_bottom:
                continue
        if col > 0:
            subblock_left = subblocks[mat[row][col - 1]]
            if subblock.edge_left != subblock_left.edge_right:
                continue

        prev_block_ids = mat[:row + 1, :col + 1].flatten()[:-1]   # TODO: double-check?
        no_id_conflict = True
        current_tile_ids = list(subblock.exist_tile_ids.keys())
        #print(f"pos: ({row},{col}), prev_block_ids: {prev_block_ids}, current_tile_ids: {current_tile_ids}")
        for prev_block_id in prev_block_ids:
            if subblocks[prev_block_id].contain_tile_ids(current_tile_ids):
                no_id_conflict = False
                break
        if not no_id_conflict:
            continue

        mat[row][col] = subblock.block_id
        block_search(depth + 1, mat, block_size, subblocks, newblocks)
        mat[row][col] = -1


def find_blocks(block_size, blocks_prev, blocks_cur):
    init_mat = np.empty((block_size, block_size), dtype=np.int32)
    init_mat.fill(-1)
    block_search(
        depth=0,
        mat=init_mat,
        block_size=block_size,
        subblocks=blocks_prev,
        newblocks=blocks_cur,
    )


def get_possible_ans(level, blocks_all, tiles_number):
    possible_ans = {}
    for block in blocks_all[level].values():
        t1 = tiles_number[block.tile_arrange[0, 0]]
        t2 = tiles_number[block.tile_arrange[0, -1]]
        t3 = tiles_number[block.tile_arrange[-1, 0]]
        t4 = tiles_number[block.tile_arrange[-1, -1]]
        ans = t1 * t2 * t3 * t4
        possible_ans[ans] = True
    return list(possible_ans.keys())


def print_level(level, blocks_all, tiles_number):
    print(f"num_solutions: {len(blocks_all[level])}")
    blocks_all[level][0].print_mat()
    blocks_all[level][0].print_edges()
    blocks_all[level][0].print_tiles()
    print(f"possible answers: {get_possible_ans(level, blocks_all, tiles_number)}")


def search_level(level, level_prev, blocks_all):
    cachefile = f"Day20/q1_{level}x{level}.pkl"
    if not os.path.exists(cachefile):
        block_size = level // level_prev
        find_blocks(block_size, blocks_all[level_prev], blocks_all[level])
        print(f"#tiles level {level}: {len(blocks_all[level])}")
        with open(cachefile, "wb") as fwrite:
            pickle.dump(blocks_all[level], fwrite)
    else:
        print("loading")
        with open(cachefile, "rb") as fread:
            blocks_all[level] = pickle.load(fread)


def search_q1(tiles_all, tiles_number, blocks_all):
    for i, tile in enumerate(tiles_all.values()):
        block = Block(block_id=i, block_size=1)
        block.init_from_tile(tile)
        blocks_all[1][i] = block

    search_level(3, 1, blocks_all)
    print_level(3, blocks_all, tiles_number)

    search_level(6, 3, blocks_all)
    print_level(6, blocks_all, tiles_number)

    search_level(12, 6, blocks_all)
    print_level(12, blocks_all, tiles_number)


def solution(lines):
    tiles_all, tiles_number = init_tiles(lines)
    blocks_all = {i: {} for i in range(1, 13)}

    search_q1(tiles_all, tiles_number, blocks_all)

    possible_ans = get_possible_ans(12, blocks_all, tiles_number)
    assert len(possible_ans) == 1
    return possible_ans[0]


def create_q2_example():
    with open(f"{CURRENT_DIR}/q2_example.txt", "r") as fread:
        matstr = fread.read().splitlines()

    image_size = len(matstr)
    print(image_size)
    image_mat = np.zeros((image_size, image_size), dtype=np.uint8)
    for y, row in enumerate(matstr):
        for x, ch in enumerate(row):
            image_mat[y][x] = 1 if ch == "." else 2
    return image_mat


def count_sea_monster(image_mat, sea_monster):
    sm_w = sea_monster.shape[1]
    sm_h = sea_monster.shape[0]
    sm_lt = []
    for y in range(image_mat.shape[0] - sm_h):
        for x in range(image_mat.shape[1] - sm_w):
            is_sm = True
            for yi in range(sm_h):
                for xi in range(sm_w):
                    if sea_monster[yi][xi] == 2 and image_mat[y + yi][x + xi] == 1:
                        is_sm = False
                        break
                if not is_sm: break
            if is_sm:
                sm_lt.append((y, x))
    for y, x in sm_lt:
        for yi in range(sm_h):
            for xi in range(sm_w):
                if sea_monster[yi][xi] == 2:
                    assert image_mat[y + yi][x + xi] > 1
                    image_mat[y + yi][x + xi] += 1
    print(f"#sea monster: {len(sm_lt)}")


def count_roughness(image_mat):
    roughness = 0
    for row in image_mat:
        for v in row:
            if v == 2:
                roughness += 1
    return roughness


def solution2(lines):
    tiles_all, tiles_number = init_tiles(lines)
    blocks_all = {i: {} for i in range(1, 13)}

    search_q1(tiles_all, tiles_number, blocks_all)

    possible_ans = get_possible_ans(12, blocks_all, tiles_number)
    assert len(possible_ans) == 1

    print("\nresult tiles:")
    blocks_all[12][0].print_tiles()
    print("result mat:")
    blocks_all[12][0].print_mat()

    # example
    #image_mat = create_q2_example()
    #tile_size = 10
    image_mat = blocks_all[12][0].block_mat
    tile_size = image_mat.shape[0] // blocks_all[12][0].tile_arrange.shape[0]

    mat_size = image_mat.shape[0]
    
    print(f"tile_size: {tile_size}")
    idx_remove = []
    for pos in range(0, mat_size + 1, tile_size):
        if 0 <= pos <= mat_size - 1:
            idx_remove.append(pos)
        if 0 <= pos - 1 <= mat_size - 1:
            idx_remove.append(pos - 1)
    print(idx_remove)
    print(f"image_mat ({image_mat.shape}): \n{image_mat}")
    image_mat = np.delete(image_mat, idx_remove, axis=0)
    image_mat = np.delete(image_mat, idx_remove, axis=1)
    print(f"slim image_mat ({image_mat.shape}): \n{image_mat}")

    sea_monster = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2],
        [1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1]
    ]
    sea_monster = np.array(sea_monster, dtype=np.uint8)

    for degree in range(90, 361, 90):
        image_mat = np.rot90(image_mat)
        count_sea_monster(image_mat, sea_monster)

        image_mat_flip = np.fliplr(image_mat)
        count_sea_monster(image_mat_flip, sea_monster)

    roughness = count_roughness(image_mat)

    return roughness


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
