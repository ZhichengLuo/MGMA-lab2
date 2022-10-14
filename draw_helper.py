
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def draw_influence_graph(G, pos, infected_nodes=[], ax=None, **kwds):
    color_map = ['#1f78b4' if n not in infected_nodes else '#ff2638' for n in list(G)]
    nx.draw_networkx(G, pos=pos, ax=ax, node_color = color_map, **kwds)

def get_slide_show_infection_process(G, infection_log, pos=None, interval=400, **kwds):
    fig, ax = plt.subplots(figsize=(15,10))
    artists = list()
    infected_so_far = list()
    track = []
    for step in infection_log:
        infected_so_far += step
        draw_influence_graph(G, pos, infected_so_far, ax, **kwds)
        art = ax.get_children()
        artists.append([a for a in art if a not in track])
        track += art
    anim = animation.ArtistAnimation(fig, artists, interval=interval, repeat_delay=1000, blit=True)
    plt.close()
    return anim