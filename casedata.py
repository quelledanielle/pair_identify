from collections import defaultdict

def count_sites(data, site1, site2, dist, d_TTT, d_FTT, freq, count):
    # exclude sites in RepeatMasker regions
    if data[site1] < 10 and data[site2] < 10:
        csv_row = "%i,%i,%i" % (site1, site2, dist)
        print csv_row
        freq[dist] += 1
        
        # in ChIP-seq region
        if data[site1] % 10 == 1:
            d_TTT.append(csv_row)
            count["TTT"] += 1
        # outside ChIP-seq region
        else:
            d_FTT.append(csv_row)
            count["FTT"] += 1

def study(data, tf1, tf2, max_dist):
    d_TTT = []
    d_FTT = []
    freq = defaultdict(int)
    count = defaultdict(int)
    
    tf1_sites = tf1.sites
    tf2_sites = tf2.sites
    
    tf1_len = tf1.num_sites
    tf2_len = tf2.num_sites
    
    l = 0
    r = 0
    
    l_seek = 0
    r_seek = 0
    
    while l < tf1_len and r < tf2_len:
        finished = l_seek >= tf1_len or r_seek >= tf2_len
        
        if not finished:
            site1 = tf1_sites[l_seek]
            site2 = tf2_sites[r_seek]
            dist = abs(site1 - site2)
        
        if not finished and dist <= max_dist:
            count_sites(data, site1, site2, dist, d_TTT, d_FTT, freq, count)
            
            if site1 >= site2:
                l_seek += 1
            else:
                r_seek += 1
        else:
            if site1 >= site2:
                r += 1
                r_seek = r
                l_seek = l
            else:
                l += 1
                l_seek = l
                r_seek = r
    
    return (d_TTT, d_FTT, freq, count)