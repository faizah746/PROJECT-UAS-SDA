import tkinter as tk
from tkinter import ttk

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class TreeGUI(tk.Tk):
    def __init__(self, root_node):
        super().__init__()
        self.title("Struktur Organisasi Rumah Sakit Islam Surabaya")
        self.geometry("900x600")

        self.root_node = root_node

        self.search_frame = tk.Frame(self)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(self.search_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(self.search_frame, text="Cari", command=self.perform_search).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(self.search_frame, text="Reset", command=self.reset_tree).pack(side=tk.LEFT)
        
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.node_refs = {}  
        self.populate_tree()
        self.style_treeview()

        self.no_result_label = tk.Label(self, text="", fg="red", bg="#e0e1dd", font=("Segoe UI", 12, "bold"))
        self.no_result_label.pack(pady=(0, 10))

     # warna GUI
    def style_treeview(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#f5f7fa",
                        foreground="#22223b",
                        rowheight=28,
                        fieldbackground="#f5f7fa",
                        font=("Segoe UI", 11))
        style.map("Treeview",
                  background=[("selected", "#b5ead7")],
                  foreground=[("selected", "#22223b")])
        style.configure("Treeview.Heading",
                        background="#22223b",
                        foreground="#f5f7fa",
                        font=("Segoe UI", 12, "bold"))
        self.configure(bg="#e0e1dd")
        self.search_frame.configure(bg="#e0e1dd")

        for child in self.search_frame.winfo_children():
            if isinstance(child, tk.Entry):
                child.configure(bg="#fcfffd", fg="#22223b", insertbackground="#22223b", relief="flat", font=("Segoe UI", 11))
            elif isinstance(child, tk.Button):
                child.configure(bg="#cf4822", fg="#f5f7fa", activebackground="#b5ead7", activeforeground="#22223b", relief="flat", font=("Segoe UI", 11, "bold"))


    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.node_refs.clear()
        self.insert_node("", self.root_node)

    def insert_node(self, parent_id, node):
        node_id = self.tree.insert(parent_id, "end", text=node.name, open=False)
        self.node_refs[node] = node_id
        for child in node.children:
            self.insert_node(node_id, child)

    def perform_search(self):
            keyword = self.search_var.get().lower()
            self.tree.delete(*self.tree.get_children())
            self.no_result_label.config(text="")

            def collect_matches(node, matches):
                if keyword in node.name.lower():
                    matches.append(node)
                for child in node.children:
                    collect_matches(child, matches)

            matches = []
            collect_matches(self.root_node, matches)

            if matches:
                for match in matches:
                    self.tree.insert("", "end", text=match.name, open=True)
            else:
                self.no_result_label.config(text="Tidak ada hasil ditemukan.")
            
            def reset_tree(self):
                self.search_var.set("")
                self.no_result_label.config(text="")
                self.populate_tree()


    def reinsert_subtree(self, node, parent_id):
        tree_id = self.tree.insert(parent_id, "end", text=node.name, open=True)
        for child in node.children:
            self.reinsert_subtree(child, tree_id)

    def reset_tree(self):
        self.search_var.set("")
        self.populate_tree()
    
    def dfs_search(node, query, path=None):
        if path is None:
            path = []
        results = []
        current_path = path + [node]
    
        if query.lower() in node.name.lower():
            results.append(current_path)
    
        for child in node.children:
            results.extend(TreeGUI.dfs_search(child, query, current_path)) 
        
        return results
    
    def build_filtered_tree(paths):
        root = Node("Hasil Pencarian")
        node_map = {}
    
        for path in paths:
            parent = root
            for node in path:
                if (id(parent), node.name) not in node_map:
                    new_node = Node(node.name)
                    parent.add_child(new_node)
                    node_map[(id(parent), node.name)] = new_node
                parent = node_map[(id(parent), node.name)]
    
        return root

direktur = Node("Direktur - Dr. H. Dodo Anondo, MPH, FISQua")

wakil_direktur = Node("Wakil Direktur")

wd_umum = Node("Wakil Direktur Umum & Keuangan – Mochammad Amsa Effendi Pohan, SE")
wd_medis = Node("Wakil Direktur Pelayanan Medis & Keperawatan - drg. Hj. Laily Rachmawati, Sp. Perio")
wd_p3 = Node("Wakil Direktur Pengembangan, Pendidikan, Penunjang Medis & SI(P3SI) - dr. Widayanti, M.Kes")

wakil_direktur.add_child(wd_umum)
wakil_direktur.add_child(wd_medis)
wakil_direktur.add_child(wd_p3)

kepala_bidang = Node("Kepala Bidang Lain")
unit_penunjang = Node("Unit Penunjang dan Fungsional")

wd_umum.add_child(Node("Kepala Bagian Keuangan – Laily Nashrijah Mashita, A.Md."))
wd_umum.add_child(Node("Kepala Seksi Keuangan & Perpajakan - Reni Mulyaningsih, S.Akt"))
wd_umum.add_child(Node("Kepala Seksi Akuntansi & Hutang Piutang - Uswatun Khasanah, SE"))
wd_umum.add_child(Node("Kepala Seksi Sekretariat – Ayu Kusuma Andriani, S.KM"))

rawat_inap = Node("Kepala Instalasi Rawat Inap - Anies Muthoharoh, S.Kep.Ns, M.Tr.Kep")
rawat_inap.add_child(Node("Kepala Ruang Makkah - Umi Kulsum, S.Kep.Ns"))
rawat_inap.add_child(Node("Kepala Ruang Makkah (lain) - Dwi Puspitasari, S.Kep.Ns"))
rawat_inap.add_child(Node("Kepala Ruang An-Nisa - Ainun Mufidah, S.ST"))
rawat_inap.add_child(Node("Kepala Ruang Ar Rayyan - Aulia Ineke R, S.Kep.Ns"))
rawat_inap.add_child(Node("Kepala Ruang Multazam - Eni Mujiati, A.Md.Kep"))
rawat_inap.add_child(Node("Kepala Ruang Madinah (Pjs.) - Tutwuri Handayani, S.Kep.Ns (Pjs.)"))
rawat_inap.add_child(Node("Kepala Ruang Al-Kautsar – Mu’minatus Syarifah, S.Kep.Ns"))
rawat_inap.add_child(Node("Kepala Ruang Ar-Radhiin – Miftahul Zamroh, S.Kep.Ns"))

rawat_jalan = Node("Kepala Instalasi Rawat Jalan - dr. Wisnu Laksmana, Sp.U")
rawat_jalan.add_child(Node("Kepala Ruang Rawat Jalan - Heny Yuliani, A.Md.Kep"))

igd = Node("Kepala IGD – dr. H. Dlorifuddin Zuhri")
igd.add_child(Node("Kepala Ruang Gawat Darurat - Budi Setiyawan, S.Kep.Ns"))

rawat_khusus = Node("Kepala Instalasi Rawat Khusus - dr. Donny Permana, Sp.OT, AIFO-K")
rawat_khusus.add_child(Node("Kepala Ruang ICU/ICCU/HCU – Bintang Eka, S.Kep.Ns"))
rawat_khusus.add_child(Node("Kepala Ruang NICU/PICU/Perina – Ayu Agustina S, S.Kep.Ns"))
rawat_khusus.add_child(Node("Kepala Ruang CSSD – Widia Ningtyas, S.Farm., Apt."))

wd_medis.add_child(rawat_inap)
wd_medis.add_child(rawat_jalan)
wd_medis.add_child(igd)
wd_medis.add_child(rawat_khusus)

pendidikan_penelitian = Node("Kepala Bagian Pendidikan, Pelatihan & Penelitian - Arie Kusumo Dewi, S.Kep.Ns")
pendidikan_penelitian.add_child(Node("Kepala Seksi Pendidikan, Pelatihan & Penelitian Eksternal (Pjs.) - Tata Mahyuvi, S.Kep.Ns (Pjs.)"))
pendidikan_penelitian.add_child(Node("Kepala Seksi Pendidikan, Pelatihan & Penelitian Internal - Eva Zulfa Nurrahmi, ST"))

SDM = Node("Kepala SDM & Pengembangan - Sri Rejeki Fitriana, S.KM & Budhi Setianto, ST, M.Kes")
SDM.add_child(Node("Kepala Seksi Pengembangan Mutu SDM Keperawatan - Yusida Achmad, S.Kep.Ns"))
SDM.add_child(Node("Kepala Seksi Pengembangan Karir - Desi Indrawati, S.KM"))

SIM = Node("Kepala SIM")
SIM.add_child(Node("Kepala Seksi SIM Aplikasi - Farris Fardiansyah, S.Kom"))
SIM.add_child(Node("Kepala Seksi SIM Jaringan & Pemeliharaan - Agung Subandi, S.Kom"))

wd_p3.add_child(pendidikan_penelitian)
wd_p3.add_child(SDM)
wd_p3.add_child(SIM)

pengembangan_pendidikan = Node("Pengembangan Pendidikan")
pengembangan_pendidikan.add_child(pendidikan_penelitian)
pengembangan_pendidikan.add_child(SDM)

layanan = Node("Kepala Bidang Layanan Medis - dr. Wiwit Pujiati Royah")
admin_medis = Node("Kepala Bagian Administrasi Medis – dr. Riska Indriani Waluyo")
admin_medis.add_child(Node("Koordinator TPPRI – Abdul Rochman, Amd.RMIK"))
admin_medis.add_child(Node("Koordinator TPPRJ – Rumianah, Amd.Kes"))
admin_medis.add_child(Node("Koordinator Kasir – Yaumil Maghfiroh, S.Sos"))
rekam_medis = Node("Kanit Rekam Medis & Administrasi – Dessy Mulyawati, Amd.PK")
komite_rekam_medis = Node("Ketua Komite Rekam Medis")
rekam_medis.add_child(komite_rekam_medis)
layanan.add_child(admin_medis)
layanan.add_child(rekam_medis)

penunjang = Node("Kepala Bidang Penunjang Medis - Dewanti Wardhani, S.Farm.Apt")
penunjang.add_child(Node("Kepala Instalasi Farmasi - Apt. Rohdiya Wahyuni, S.Farm"))
penunjang.add_child(Node("Kepala Instalasi Radiologi - Arta Dewi Nurani Hasan, S.Tr.Kes"))
penunjang.add_child(Node("Kepala Instalasi Laboratorium - dr. Nathalya Dwi Kartika Sari, Sp.PK"))
penunjang.add_child(Node("Kepala Instalasi Gizi - Emi Nur Muslimah, Amd.Gz"))
penunjang.add_child(Node("Kepala Ruang Laboratorium – Siti Habibba, A.Md.AK"))
penunjang.add_child(Node("Kepala Ruang Pengelolaan & Perbekalan Farmasi – Apt. Frinka Martha R, S.Farm"))

pemeliharaan = Node("Pemeliharaan Sarana")
pemeliharaan.add_child(Node("Kepala Seksi Pemeliharaan Sarana Medis - Andhie Kusuma, ST"))
pemeliharaan.add_child(Node("Kepala Seksi Pemeliharaan Sarana Umum - Rahmatullah, S.Pd"))
pemeliharaan.add_child(Node("Kepala Seksi Pemeliharaan Sarana Elektro (Pjs.) - Tommy Eka Putra Bimantara, ST (Pjs.)"))
pemeliharaan.add_child(Node("Kepala Seksi Keamanan & Ketertiban (Kamtib) - Ainur Rofiq"))

keperawatan = Node("Kepala Bidang Keperawatan - Sumiati, S.Kep.Ns")
keperawatan.add_child(Node("Kepala Seksi Asuhan & Pelayanan Keperawatan - Sulistyorini, S.Kep.Ns, M.Tr.Kep"))
keperawatan.add_child(Node("Kepala Ruang Kamar Operasi - Achmad Dailami, S.Kep.Ns"))
keperawatan.add_child(Node("Pj Home Care - Tri Wi Untari, A.Md.Kep"))

humas = Node("Kepala Seksi Humas (Pjs.) - drg. Dian Permata Asri (Pjs.)")

kepala_bidang.add_child(layanan)
kepala_bidang.add_child(penunjang)
kepala_bidang.add_child(pemeliharaan)
kepala_bidang.add_child(keperawatan)
kepala_bidang.add_child(humas)

unit_penunjang = Node("Unit Penunjang dan Fungsional")
unit_penunjang.add_child(Node("Kepala Seksi BPJS & Verifikasi - Yunita Anggrahini, S.Pd"))
unit_penunjang.add_child(Node("Kepala Ruang Fisioterapi - Silia Kuswendini, Amd.Fis"))
unit_penunjang.add_child(Node("Kepala Ruang Hemodialisa - Destyorini, S.Kep.Ns"))
unit_penunjang.add_child(Node("Kepala Seksi Logistik Umum (Pjs.) - Fitria Suryaningrum, SE (Pjs.)"))
unit_penunjang.add_child(Node("Kepala Seksi Layanan Transportasi - Mochamad Dyan E.R.W, S.KM"))
unit_penunjang.add_child(Node("Kepala Seksi Pemasaran - Aprilya Eka Susianti, SE, MM"))
unit_penunjang.add_child(Node("Kepala Satuan Pemeriksaan Internal (SPI) – Yulia Zahro, SE"))
unit_penunjang.add_child(Node("Kepala Bagian Umum – Dini Kharisma Sari, S.KM"))
unit_penunjang.add_child(Node("Kepala Seksi Bina Rohani – Dra. Maslahah"))
unit_penunjang.add_child(Node("Kepala Instalasi PKRS – Giantina Amalia, S.KM"))
unit_penunjang.add_child(Node("Kepala Seksi Kesehatan Lingkungan – Kusumayanti, Amd.KL"))


komite_rumah_sakit = Node("Komite Rumah Sakit")
komite_rumah_sakit.add_child(Node("Ketua Komite Medik – dr. Hartatiek Nila Kamila, Sp.OG"))
komite_rumah_sakit.add_child(Node("Ketua Komite Keperawatan – M.Fatkan, S.Kep.Ns"))
komite_rumah_sakit.add_child(Node("Ketua Komite Tenaga Kesehatan Lain – Apt. Dewanti Wardhani, S.Farm"))
komite_rumah_sakit.add_child(Node("Ketua Komite Etik dan Hukum – dr. Bony Pramono, Sp.A"))
komite_rumah_sakit.add_child(Node("Ketua Komite Koordinator Pendidik – dr. Nathalya Dwi Kartika Sari, Sp.PK"))
komite_rumah_sakit.add_child(Node("Ketua Komite Rekam Medis – dr. Riska Indriani Waluyo"))
komite_rumah_sakit.add_child(Node("Ketua Komite Program Pengendalian Resistensi Antimikroba – dr. Wisnu Laksamana, Sp.U"))
komite_rumah_sakit.add_child(Node("Ketua Komite Farmasi dan Terapi – dr. Agus Prabowo, Sp.PD"))
komite_rumah_sakit.add_child(Node("Ketua Komite Kesehatan dan Keselamatan Kerja – Ahmad Qamarudin Jamil, S.KM"))
komite_rumah_sakit.add_child(Node("Ketua Komite Mutu – Aida Rahmatari, S.KM"))
komite_rumah_sakit.add_child(Node("Ketua Komite Pencegahan Pengendalian Infeksi – dr. Sigit Wijanarko, Sp.B"))
komite_rumah_sakit.add_child(Node("Ketua Komite Etik Penelitian – dr. Indah Purnamasari, Sp.DV, M.Ked.Klin."))

mod_group = Node("Manager On Duty (MOD)")
mod_group.add_child(Node("MOD - Siti Rokhimah, Amd.Kep"))
mod_group.add_child(Node("MOD - Abdul Shomad, Amd.Kep"))
mod_group.add_child(Node("MOD - Nuraeni"))
mod_group.add_child(Node("MOD - Anis Rosyidah, S.ST"))
mod_group.add_child(Node("MOD - SYAPII, S.Kep.Ns"))

manajer_pelayanan = Node("Manajer Pemberi Pelayanan (MPP)")
manajer_pelayanan.add_child(Node("MPP - Fridayanti, S.Kep.Ns"))
manajer_pelayanan.add_child(Node("MPP - Miftahul Zamroh, S.Kep.Ns"))

unit_penunjang.add_child(mod_group)
unit_penunjang.add_child(manajer_pelayanan)

direktur.add_child(wakil_direktur)
direktur.add_child(kepala_bidang)
direktur.add_child(unit_penunjang)
direktur.add_child(komite_rumah_sakit)

if __name__ == "__main__":
    app = TreeGUI(direktur)
    app.mainloop()
