end_result = ''
_failed = False
_failed_msg = ''


def sha_256(entry=None):
    global _failed
    global _failed_msg
    entry = input('\n' + f"Enter anything up to {512 - 65} bits : ")
    print(f'Entry : {entry}')
    constants()
    binary = '0' + '0'.join(format(ord(i), 'b') for i in entry)
    if len(binary) > 512 - 65:
        _failed = True
        _failed_msg = f'Error : maximum bit length is {512 - 65}, but {len(binary)} has been entered'
        #print('\n' + f'Error : maximum bit length is {512 - 65}, but {len(binary)} has been entered')
        pass
    else:
        _failed = False
        print(f"The length of the entry is : {len(binary)} bits | [{binary}]")
        padding(binary)
        return binary


def constants():
    const = []
    for n in range(2, 312):
        prime = True
        for i in range(2, n):
            if n % i == 0:
                prime = False
        if prime:
            cube_root = n ** (1 / 3)
            cube_root %= int(cube_root)
            cube_root *= 2 ** 32
            binary = '{:032b}'.format(int(cube_root))
            const.append(binary)
    return const


def padding(binary):
    target = 512
    block_number = (len(binary) // 448) + 1
    target *= block_number
    length = len(binary)
    binary += '1'
    for i in range(0, (target - 65 - length)):
        binary += '0'
    binary += (64 - len(format(length, 'b'))) * '0' + (format(length, 'b'))
    message_schedule(binary)


def message_schedule(block):
    schedule = []
    p = 0
    for i in range(0, 16):
        schedule.append(block[0 + p:32 + p])
        p += len(block) // 16
    add_to_schedule(schedule)
    return schedule


def shift_r(n, word):
    for i in range(0, n):
        word = '0' + word
        word = word[:-1:]
    return word


def rotate_r(n, word):
    for i in range(0, n):
        word = word[-1] + word
        word = word[:-1:]
    return word


def sigma_0(word):
    ans = ''
    l1 = rotate_r(7, word)
    l2 = rotate_r(18, word)
    l3 = shift_r(3, word)
    for i in range(0, len(word)):
        if int(l1[i]) + int(l2[i]) + int(l3[i]) == 1 or int(l1[i]) + int(l2[i]) + int(l3[i]) == 3:
            ans += '1'
        else:
            ans += '0'
    return ans


def sigma_1(word):
    ans = ''
    l1 = rotate_r(17, word)
    l2 = rotate_r(19, word)
    l3 = shift_r(10, word)
    for i in range(0, len(word)):
        if int(l1[i]) + int(l2[i]) + int(l3[i]) == 1 or int(l1[i]) + int(l2[i]) + int(l3[i]) == 3:
            ans += '1'
        else:
            ans += '0'
    return ans


def sigma_up_0(word):
    ans = ''
    l1 = rotate_r(2, word)
    l2 = rotate_r(13, word)
    l3 = rotate_r(22, word)
    for i in range(0, len(word)):
        if int(l1[i]) + int(l2[i]) + int(l3[i]) == 1 or int(l1[i]) + int(l2[i]) + int(l3[i]) == 3:
            ans += '1'
        else:
            ans += '0'
    return ans


def sigma_up_1(word):
    ans = ''
    l1 = rotate_r(6, word)
    l2 = rotate_r(11, word)
    l3 = rotate_r(25, word)
    for i in range(0, len(word)):
        if int(l1[i]) + int(l2[i]) + int(l3[i]) == 1 or int(l1[i]) + int(l2[i]) + int(l3[i]) == 3:
            ans += '1'
        else:
            ans += '0'
    return ans


def choice(x, y, z):
    ans = ''
    for i in range(0, len(x)):
        if x[i] == '1':
            ans += y[i]
        else:
            ans += z[i]
    return ans


def majority(x, y, z):
    ans = ''
    l1 = x
    l2 = y
    l3 = z
    for i in range(0, len(x)):
        if int(l1[i]) + int(l2[i]) + int(l3[i]) <= 1:
            ans += '0'
        else:
            ans += '1'
    return ans


def add_to_schedule(schedule):
    for i in range(64 - 16):
        new_block = bin(
            int(sigma_1(schedule[-2]), 2) + int(schedule[-7], 2) + int(sigma_0(schedule[-15]), 2) + int(schedule[-16],
                                                                                                        2))
        new_block = int(new_block, 2) % 2 ** 32
        binary = '{:032b}'.format(int(new_block))
        schedule.append(str(binary))
    compression(constants(), registry_constants(), schedule)
    return schedule


def registry_constants():
    const = []
    a = int(2 ** (1 / 2) % int(2 ** (1 / 2)) * 2 ** 32)
    b = int(3 ** (1 / 2) % int(3 ** (1 / 2)) * 2 ** 32)
    c = int(5 ** (1 / 2) % int(5 ** (1 / 2)) * 2 ** 32)
    d = int(7 ** (1 / 2) % int(7 ** (1 / 2)) * 2 ** 32)
    e = int(11 ** (1 / 2) % int(11 ** (1 / 2)) * 2 ** 32)
    f = int(13 ** (1 / 2) % int(13 ** (1 / 2)) * 2 ** 32)
    g = int(17 ** (1 / 2) % int(17 ** (1 / 2)) * 2 ** 32)
    h = int(19 ** (1 / 2) % int(19 ** (1 / 2)) * 2 ** 32)
    var = [a, b, c, d, e, f, g, h]
    for i in var:
        binary = '{:032b}'.format(int(i))
        const.append(binary)
    return const


def compression(const, r_const, schedule):
    for i in range(len(schedule)):
        temp1 = bin(
            int(sigma_up_1(r_const[4]), 2) + int(choice(r_const[4], r_const[5], r_const[6]), 2) + int(r_const[-1], 2) +
            int(schedule[i], 2) + int(const[i], 2))
        temp1 = int(temp1, 2) % 2 ** 32
        temp1 = '{:032b}'.format(int(temp1))
        temp2 = bin(int(sigma_up_0(r_const[0]), 2) + int(majority(r_const[0], r_const[1], r_const[2]), 2))
        temp2 = int(temp2, 2) % 2 ** 32
        temp2 = '{:032b}'.format(int(temp2))
        temp = bin(int(temp1, 2) + int(temp2, 2))
        temp = int(temp, 2) % 2 ** 32
        temp = '{:032b}'.format(int(temp))
        r_const.insert(0, temp)
        r_const.pop(-1)
        e_add = bin(int(temp1, 2) + int(r_const[4], 2))
        e_add = int(e_add, 2) % 2 ** 32
        e_add = '{:032b}'.format(int(e_add))
        r_const.pop(4)
        r_const.insert(4, e_add)
    org = registry_constants()
    end_ex = []
    for i in range(len(org)):
        r_const_add = bin(int(org[i], 2) + int(r_const[i], 2))
        r_const_add = int(r_const_add, 2) % 2 ** 32
        r_const_add = '{:032b}'.format(int(r_const_add))
        end_ex.append(r_const_add)
    result(end_ex)
    return end_ex


def result(end_ex):
    global end_result
    digest = []
    for i in end_ex:
        ans = int(i, 2)
        digest.append((hex(ans)[2:]))
    end_result = ''.join(digest)
    print(f'The hash of the entry is : {end_result}')
    return end_result

if __name__ == "__main__":
    sha_256()
input("Press 'ENTER' to close")

