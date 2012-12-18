%define dracutlibdir %{_prefix}/lib/dracut

# Variables must be defined
%define with_nbd                1

# nbd in Fedora only
%if 0%{?rhel} >= 6
%define with_nbd 0
%endif

Name: dracut
Version: 024
Release: 15.git20121218%{?dist}

Summary: Initramfs generator using udev
%if 0%{?fedora} || 0%{?rhel}
Group: System Environment/Base
%endif
%if 0%{?suse_version}
Group: System/Base
%endif

# The entire source code is GPLv2+
# except install/* which is LGPLv2.1+
License: GPLv2+ and LGPLv2.1+

URL: https://dracut.wiki.kernel.org/

# Source can be generated by
# http://git.kernel.org/?p=boot/dracut/dracut.git;a=snapshot;h=%{version};sf=tgz
Source0: http://www.kernel.org/pub/linux/utils/boot/dracut/dracut-%{version}.tar.bz2
Patch1: 0001-dracut.sh-only-save-kernel_cmdline-if-set.patch
Patch2: 0002-dracut.conf.d-fedora.conf.example-s-kernelcmdline-ke.patch
Patch3: 0003-40network-ifup.sh-do_static-and-do_ipv6auto-return-0.patch
Patch4: 0004-dracut.sh-only-warn-not-error-if-we-don-t-strip.patch
Patch5: 0005-dracut.sh-do-not-strip-signed-kernel-modules.patch
Patch6: 0006-i18n-parse-i18n.sh-fix-locale.conf-caused-by-4dbc1d1.patch
Patch7: 0007-network-fixed-MAC-address-assignment.patch
Patch8: 0008-dmsquash-live-add-systemd-checkisomd5-service.patch
Patch9: 0009-crypt-crypt-run-generator.sh-do-not-timeout-for-LUKS.patch
Patch10: 0010-systemd-dracut-cmdline.service-run-before-systemd-vc.patch
Patch11: 0011-add-swapoff-to-initramfs-to-fix-shutdown-reboot.patch
Patch12: 0012-dracut.spec-add-iputils-and-iproute-requirement-for-.patch
Patch13: 0013-nfs-nfsroot-cleanup.sh-mount-bind-instead-of-move.patch
Patch14: 0014-iscsi-iscsiroot.sh-reload-rules-after-adding-99-iscs.patch


BuildRequires: dash bash git

%if 0%{?fedora} || 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
%if 0%{?suse_version}
BuildRoot: %{_tmppath}/%{name}-%{version}-build
%endif

%if 0%{?fedora} || 0%{?rhel}
BuildRequires: docbook-style-xsl docbook-dtds libxslt
%endif

%if 0%{?suse_version}
-BuildRequires: docbook-xsl-stylesheets libxslt
%endif

BuildRequires: asciidoc

%if 0%{?fedora} > 12 || 0%{?rhel}
# no "provides", because dracut does not offer
# all functionality of the obsoleted packages
Obsoletes: mkinitrd <= 6.0.93
Obsoletes: mkinitrd-devel <= 6.0.93
Obsoletes: nash <= 6.0.93
Obsoletes: libbdevid-python <= 6.0.93
%endif

%if 0%{?fedora} > 16 || 0%{?rhel} > 6
BuildRequires: systemd-units
%endif

%if 0%{?suse_version} > 9999
Obsoletes: mkinitrd < 2.6.1
Provides: mkinitrd = 2.6.1
%endif

Obsoletes: dracut-kernel < 005
Provides:  dracut-kernel = %{version}-%{release}

Requires: bash
Requires: coreutils
Requires: cpio
Requires: filesystem >= 2.1.0
Requires: findutils
Requires: grep
Requires: hardlink
Requires: gzip xz
Requires: module-init-tools >= 3.7-9
Requires: sed
Requires: file
Requires: kpartx
Requires: udev > 166
Requires: kbd kbd-misc
%if 0%{?fedora} || 0%{?rhel} > 6
Requires: util-linux >= 2.21
Conflicts: systemd < 187
%else
Requires: util-linux-ng >= 2.21
%endif

%if 0%{?fedora} || 0%{?rhel} > 6
Conflicts: initscripts < 8.63-1
Conflicts: plymouth < 0.8.0-0.2009.29.09.19.1
%endif

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%package network
Summary: dracut modules to build a dracut initramfs with network support
Requires: %{name} = %{version}-%{release}
Requires: iputils
Requires: iproute
Obsoletes: dracut-generic < 008
Provides:  dracut-generic = %{version}-%{release}

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?suse_version}
%package fips
Summary: dracut modules to build a dracut initramfs with an integrity check
Requires: %{name} = %{version}-%{release}
Requires: hmaccalc
%if 0%{?rhel} > 5
# For Alpha 3, we want nss instead of nss-softokn
Requires: nss
%else
Requires: nss-softokn
%endif
Requires: nss-softokn-freebl

%description fips
This package requires everything which is needed to build an
all purpose initramfs with dracut, which does an integrity check.
%endif

%package fips-aesni
Summary: dracut modules to build a dracut initramfs with an integrity check with aesni-intel
Requires: %{name}-fips = %{version}-%{release}

%description fips-aesni
This package requires everything which is needed to build an
all purpose initramfs with dracut, which does an integrity check
and adds the aesni-intel kernel module.

%package caps
Summary: dracut modules to build a dracut initramfs which drops capabilities
Requires: %{name} = %{version}-%{release}
Requires: libcap

%description caps
This package requires everything which is needed to build an
all purpose initramfs with dracut, which drops capabilities.

%package tools
Summary: dracut tools to build the local initramfs
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%prep
%setup -q -n %{name}-%{version}

%if %{defined PATCH1}
git init
git config user.email "dracut-maint@redhat.com"
git config user.name "Fedora dracut team"
git add .
git commit -a -q -m "%{version} baseline."

# Apply all the patches.
git am -p1 %{patches}
%endif

%build
make all

%install
%if 0%{?fedora} || 0%{?rhel}
rm -rf $RPM_BUILD_ROOT
%endif
make install DESTDIR=$RPM_BUILD_ROOT \
     libdir=%{_prefix}/lib \
     bindir=%{_bindir} \
%if %{defined _unitdir}
     systemdsystemunitdir=%{_unitdir} \
%endif
     sysconfdir=/etc mandir=%{_mandir}

echo "DRACUT_VERSION=%{version}-%{release}" > $RPM_BUILD_ROOT/%{dracutlibdir}/dracut-version.sh

%if 0%{?fedora} == 0 && 0%{?rhel} == 0 && 0%{?suse_version} == 0
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/01fips
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/02fips-aesni
%endif

# we do not support dash in the initramfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/50gensplash

%if %{defined _unitdir}
# with systemd IMA and selinux modules do not make sense
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/96securityfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/97masterkey
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/98integrity
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/98selinux
%endif

mkdir -p $RPM_BUILD_ROOT/boot/dracut
mkdir -p $RPM_BUILD_ROOT/var/lib/dracut/overlay
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
touch $RPM_BUILD_ROOT%{_localstatedir}/log/dracut.log
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/initramfs

%if 0%{?fedora} || 0%{?rhel} || 0%{?suse_version}
install -m 0644 dracut.conf.d/fedora.conf.example $RPM_BUILD_ROOT/etc/dracut.conf.d/01-dist.conf
install -m 0644 dracut.conf.d/fips.conf.example $RPM_BUILD_ROOT/etc/dracut.conf.d/40-fips.conf
%endif

%if 0%{?suse_version}
install -m 0644 dracut.conf.d/suse.conf.example   $RPM_BUILD_ROOT/etc/dracut.conf.d/01-dist.conf
%endif

%if 0%{?fedora} <= 12 && 0%{?rhel} < 6 && 0%{?suse_version} <= 9999
rm $RPM_BUILD_ROOT%{_bindir}/mkinitrd
rm $RPM_BUILD_ROOT%{_bindir}/lsinitrd
%endif

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0644 dracut.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/dracut_log

# create compat symlink
mkdir -p $RPM_BUILD_ROOT/sbin
ln -s /usr/bin/dracut $RPM_BUILD_ROOT/sbin/dracut

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README HACKING TODO COPYING AUTHORS NEWS dracut.html dracut.png dracut.svg
%{_bindir}/dracut
# compat symlink
/sbin/dracut
%if 0%{?fedora} > 12 || 0%{?rhel} >= 6 || 0%{?suse_version} > 9999
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%endif
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/dracut-functions.sh
%{dracutlibdir}/dracut-functions
%{dracutlibdir}/dracut-version.sh
%{dracutlibdir}/dracut-logger.sh
%{dracutlibdir}/dracut-initramfs-restore
%{dracutlibdir}/dracut-install
%config(noreplace) /etc/dracut.conf
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel}
%config /etc/dracut.conf.d/01-dist.conf
%endif
%dir /etc/dracut.conf.d
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/*service.8*
%if 0%{?fedora} > 12 || 0%{?rhel} >= 6 || 0%{?suse_version} > 9999
%{_mandir}/man8/mkinitrd.8*
%{_mandir}/man1/lsinitrd.1*
%endif
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*
%{dracutlibdir}/modules.d/00bootchart
%{dracutlibdir}/modules.d/04watchdog
%{dracutlibdir}/modules.d/05busybox
%{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/30convertfs
%{dracutlibdir}/modules.d/45url-lib
%{dracutlibdir}/modules.d/50plymouth
%{dracutlibdir}/modules.d/80cms
%{dracutlibdir}/modules.d/90btrfs
%{dracutlibdir}/modules.d/90crypt
%{dracutlibdir}/modules.d/90dm
%{dracutlibdir}/modules.d/90dmraid
%{dracutlibdir}/modules.d/90dmsquash-live
%{dracutlibdir}/modules.d/90kernel-modules
%{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90multipath
%{dracutlibdir}/modules.d/90qemu
%{dracutlibdir}/modules.d/91crypt-gpg
%{dracutlibdir}/modules.d/91crypt-loop
%{dracutlibdir}/modules.d/95debug
%{dracutlibdir}/modules.d/95resume
%{dracutlibdir}/modules.d/95rootfs-block
%{dracutlibdir}/modules.d/95dasd
%{dracutlibdir}/modules.d/95dasd_mod
%{dracutlibdir}/modules.d/95fstab-sys
%{dracutlibdir}/modules.d/95zfcp
%{dracutlibdir}/modules.d/95terminfo
%{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95virtfs
%if %{undefined _unitdir}
%{dracutlibdir}/modules.d/96securityfs
%{dracutlibdir}/modules.d/97masterkey
%{dracutlibdir}/modules.d/98selinux
%{dracutlibdir}/modules.d/98integrity
%endif
%{dracutlibdir}/modules.d/97biosdevname
%{dracutlibdir}/modules.d/98ecryptfs
%{dracutlibdir}/modules.d/98pollcdrom
%{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98systemd
%{dracutlibdir}/modules.d/98usrmount
%{dracutlibdir}/modules.d/99base
%{dracutlibdir}/modules.d/99fs-lib
%{dracutlibdir}/modules.d/99img-lib
%{dracutlibdir}/modules.d/99shutdown
%config(noreplace) /etc/logrotate.d/dracut_log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%if %{defined _unitdir}
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/shutdown.target.wants/dracut-shutdown.service
%endif

%files network
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/40network
%{dracutlibdir}/modules.d/95fcoe
%{dracutlibdir}/modules.d/95iscsi
%{dracutlibdir}/modules.d/90livenet
%{dracutlibdir}/modules.d/90qemu-net
%{dracutlibdir}/modules.d/95cifs
%{dracutlibdir}/modules.d/95nbd
%{dracutlibdir}/modules.d/95nfs
%{dracutlibdir}/modules.d/95ssh-client
%{dracutlibdir}/modules.d/45ifcfg
%{dracutlibdir}/modules.d/95znet

%if 0%{?fedora} || 0%{?rhel} || 0%{?suse_version}
%files fips
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/01fips
%config(noreplace) /etc/dracut.conf.d/40-fips.conf
%endif

%files fips-aesni
%defattr(-,root,root,0755)
%doc COPYING
%{dracutlibdir}/modules.d/02fips-aesni

%files caps
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/02caps

%files tools
%defattr(-,root,root,0755)
%{_mandir}/man8/dracut-catimages.8*
%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay

%changelog
* Tue Dec 18 2012 Harald Hoyer <harald@redhat.com> 024-15.git20121218
- fixed mediacheck
Resolves: rhbz#874486
- fixed mount move of rpc_pipefs
Resolves: rhbz#860525
- add "timeout=0" to /etc/crypttab in the initramfs
Resolves: rhbz#881670

* Wed Nov 21 2012 Harald Hoyer <harald@redhat.com> 024-10.git20121121
- do not strip signed kernel modules
Resolves: rhbz#873796

* Fri Oct 19 2012 Harald Hoyer <harald@redhat.com> 024-5.git20121019
- only 'warn' not 'error', if we don't strip the initramfs

* Fri Oct 19 2012 Harald Hoyer <harald@redhat.com> 024-4.git20121019
- fix ifup exit code
- fixed default "rd.auto" parameter setting

* Tue Oct 16 2012 Harald Hoyer <harald@redhat.com> 024-1
- version 024
- do not overwrite ifcfg from anaconda
- ssh-client module fixes
- added "rd.
- strip binaries in the initramfs by default now
- fixes for systemd and crypto
- new dracut kernel command line options "rd.auto"
- new dracut kernel command line options "rd.noverifyssl"
- new dracut option "--kernel-cmdline" and "kernel_cmdline" option for default parameters
- fix for kexec in shutdown, if not included in initramfs

* Thu Sep 27 2012 Harald Hoyer <harald@redhat.com> 023-65.git20120927
- no more iscsi_wait_scan
- curl: give info what URL failed, support https
- use findmnt
- systemd: wait for cryptroot
- only install crypttab in host-only mode
- add udev groups
- fixed busybox install
- fixed rd.luks.allow-discards manpage and handling
- force install dm_mod
- do not create the initramfs world reabable
- add nameserver even for dhcp
- fallback to reboot if shutdown was called without a parameter

* Mon Sep 10 2012 Harald Hoyer <harald@redhat.com> 023-39.git20120910
- fixed FIPS
- nbd port fix
- set IPV6INIT in ifcfg
- apply live updates for /run as well
- install all nfs modules

* Thu Aug 30 2012 Adam Williamson <awilliam@redhat.com> 023-21.git20120823
- add patches for updates.img and splitsep from wwoods (alpha-critical)

* Thu Aug 23 2012 Harald Hoyer <harald@redhat.com> 023-20.git20120823
- assemble nested md raids
- add z-series kernel modules
- add ping and ping6
- add "--devices" and wait for those devs to appear

* Tue Aug 21 2012 Harald Hoyer <harald@redhat.com> 023-13.git20120821
- reintroduce rd.neednet, which reenables anaconda networking
- fix some dracut-install corner cases
- fix FIPS for /boot not on extra partition

* Wed Aug 01 2012 Dennis Gilmore <dennis@ausil.us> - 023-2
- add patch to include omap_hsmmc for arm

* Wed Aug 01 2012 Harald Hoyer <harald@redhat.com> 023-1
- version 023

* Mon Jul 30 2012 Harald Hoyer <harald@redhat.com> 022-99.git20120730
- removed install of missing finished-ask-password.sh

* Mon Jul 30 2012 Harald Hoyer <harald@redhat.com> 022-97.git20120730
- moved crypt setup to systemd units

* Fri Jul 27 2012 Harald Hoyer <harald@redhat.com> 022-63.git20120727
- fixed dracut-install bug if /var/tmp contains a symlink
- fixed some partx issues

* Mon Jul 23 2012 Harald Hoyer <harald@redhat.com> 022-5.git20120723
- dracut.8: added more documentation about executing dracut

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 022-2.git20120720
- fixed some race condition for resume from hibernation

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 022-1
- version 022
- host-only kernel modules fix

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 021-1
- version 21
- systemd in the initramfs reenabled
- new option "--kver"

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 020-97.git20120717
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Harald Hoyer <harald@redhat.com> 020-96.git20120717
- disabled systemd in the initramfs, until it works correctly

* Wed Jul 11 2012 Harald Hoyer <harald@redhat.com> 020-84.git20120711
- add back "--force" to switch-root, otherwise systemd umounts /run

* Wed Jul 11 2012 Harald Hoyer <harald@redhat.com> 020-83.git20120711
- more systemd journal fixes
- nfs module fix
- install also /lib/modprobe.d/*
- fixed dracut-shutdown service
- safeguards for dracut-install
- for --include also copy symlinks

* Tue Jul 10 2012 Harald Hoyer <harald@redhat.com> 020-72.git20120710
- stop journal rather than restart
- copy over dracut services to /run/systemd/system

* Tue Jul 10 2012 Harald Hoyer <harald@redhat.com> 020-70.git20120710
- more systemd unit fixups
- restart systemd-journald in switch-root post
- fixed dracut-install loader ldd error message

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-64.git20120709
- fixed plymouth install
- fixed resume
- fixed dhcp
- no dracut systemd services installed in the system

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-57.git20120709
- more fixups for systemd-udevd unit renaming

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-55.git20120709
- require systemd >= 186
- more fixups for systemd-udevd unit renaming

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-52.git20120709
- fixed prefix in 01-dist.conf

* Fri Jul 06 2012 Harald Hoyer <harald@redhat.com> 020-51.git20120706
- cope with systemd-udevd unit renaming
- fixed network renaming
- removed dash module

* Mon Jul 02 2012 Harald Hoyer <harald@redhat.com> 020-22.git20120702
- fixed kernel modules install

* Mon Jul 02 2012 Harald Hoyer <harald@redhat.com> 020-21.git20120702
- moved /usr/bin/dracut-install to /usr/lib
- more speedups

* Fri Jun 29 2012 Harald Hoyer <harald@redhat.com> 020-1
- version 020
- new /usr/bin/dracut-install tool
- major speedup of the image creation

* Mon Jun 25 2012 Harald Hoyer <harald@redhat.com> 019-92.git20120625
- support vlan tagged binding
- speedup initramfs emergency service
- speedup image creation
- fix installkernel() return codes
Resolves: rhbz#833256
- add qemu and qemu-net modules to add qemu drivers even in host-only
- speedup btrfs and xfs fsck (nop)
- no more mknod in the initramfs (fixes plymouth on s390)

* Thu Jun 21 2012 Harald Hoyer <harald@redhat.com> 019-62.git20120621
- do not require pkg-config for systemd
- i18n fixes
- less systemd services in the initramfs

* Thu Jun 21 2012 Harald Hoyer <harald@redhat.com> 019-57.git20120620
- systemd is now the default init in the initramfs

* Mon Jun 18 2012 Harald Hoyer <harald@redhat.com> 019-40.git20120618
- new upstream version

* Mon Jun 11 2012 Harald Hoyer <harald@redhat.com> 019-16.git20120611
- new upstream version

* Tue Jun 05 2012 Dennis Gilmore <dennis@ausil.us> 019-2
- include omapdrm with the arm modules

* Mon Jun 04 2012 Harald Hoyer <harald@redhat.com> 019-1
- version 019-1

* Tue May 22 2012 Harald Hoyer <harald@redhat.com> 018-74.git20120522
- new upstream version

* Thu May 17 2012 Dennis Gilmore <dennis@ausil.us> 018-53.git20120509
- add patch to pull in arm storage modules

* Wed May 09 2012 Harald Hoyer <harald@redhat.com> 018-52.git20120509
- new upstream version

* Fri May 04 2012 Harald Hoyer <harald@redhat.com> 018-40.git20120504
- new upstream version

* Wed Apr 25 2012 Harald Hoyer <harald@redhat.com> 018-37.git20120425.1
- fixup for multipath and iscsi host-only detection

* Wed Apr 25 2012 Harald Hoyer <harald@redhat.com> 018-37.git20120425
- fixed udevd location

* Tue Apr 24 2012 Harald Hoyer <harald@redhat.com> 018-33.git20120424
- new upstream version

* Thu Apr 19 2012 Harald Hoyer <harald@redhat.com> 018-25.git20120419
- fixed network for non-network root (like installer media)

* Wed Apr 18 2012 Harald Hoyer <harald@redhat.com> 018-22.git20120418
- new upstream version

* Mon Apr 16 2012 Harald Hoyer <harald@redhat.com> 018-12.git20120416
- new upstream version, which fixes various anaconda loader issues

* Thu Apr 05 2012 Harald Hoyer <harald@redhat.com> 018-1
- version 018

* Thu Mar 22 2012 Harald Hoyer <harald@redhat.com> 017-62.git20120322
- fixed /run prefix copying

* Wed Mar 21 2012 Harald Hoyer <harald@redhat.com> 017-59.git20120321
- new upstream version, which fixes various anaconda loader issues

* Mon Mar 12 2012 Harald Hoyer <harald@redhat.com> 017-43.git20120312
- live image: fixed image uncompression
- live updates for livenet

* Thu Mar 08 2012 Harald Hoyer <harald@redhat.com> 017-40.git20120308
- add s390 ctcm network kernel module

* Thu Mar 08 2012 Harald Hoyer <harald@redhat.com> 017-39.git20120308
- kill dhclient silently
- cleanup and fix network config writeout to /run/initramfs/state
Resolves: rhbz#799989
- various cleanups

* Fri Mar 02 2012 Harald Hoyer <harald@redhat.com> 017-22.git20120302
- nfs path fixes for live image over nfs
  root=live:nfs://10.10.10.10:/srv/all/install.img ip=dhcp rd.neednet

* Thu Mar 01 2012 Harald Hoyer <harald@redhat.com> 017-19.git20120301
- fixed include of some kernel modules

* Wed Feb 29 2012 Harald Hoyer <harald@redhat.com> 017-17.git20120229
- update to latest git
- fixes for convertfs (/usr-move)

* Fri Feb 24 2012 Harald Hoyer <harald@redhat.com> 017-1
- version 017

* Fri Feb 17 2012 Harald Hoyer <harald@redhat.com> 016-9.git20120217
- update to latest git

* Wed Feb 15 2012 Harald Hoyer <harald@redhat.com> 016-1
- version 016

* Mon Feb 13 2012 Harald Hoyer <harald@redhat.com> 015-9.git20120213
- update to latest git

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 015-9.git20120210
- fix dependency loop in systemd service files

* Fri Feb 10 2012 Harald Hoyer <harald@redhat.com> 015-8.git20120210
- update to latest git

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 015-7.git20120209
- update to latest git

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 015-4.git20120209
- update to latest git

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 015-3.git20120208
- update to latest git

* Tue Feb 07 2012 Harald Hoyer <harald@redhat.com> 015-1
- version 015

* Thu Feb 02 2012 Harald Hoyer <harald@redhat.com> 014-81.git20120202
- update to latest git

* Thu Feb 02 2012 Harald Hoyer <harald@redhat.com> 014-80.git20120202
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-77.git20120126.1
- rebuild for rawhide

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-77.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-76.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-75.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-74.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-73.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-72.git20120126
- update to latest git

* Mon Jan 23 2012 Harald Hoyer <harald@redhat.com> 014-65.git20120123
- update to latest git

* Mon Jan 23 2012 Harald Hoyer <harald@redhat.com> 014-61.git20120123
- update to latest git

* Tue Jan 17 2012 Harald Hoyer <harald@redhat.com> 014-38.git20120117
- update to latest git

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 014-10.git20111215
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Harald Hoyer <harald@redhat.com> 014-9.git20111215
- update to latest git
- lots of patch changes

* Fri Oct 21 2011 Harald Hoyer <harald@redhat.com> 013-100.git20111021
- update to latest git

* Thu Oct 20 2011 Harald Hoyer <harald@redhat.com> 013-93.git20111020
- update to latest git

* Wed Oct 19 2011 Harald Hoyer <harald@redhat.com> 013-85.git20111019
- update to latest git

* Tue Oct 04 2011 Harald Hoyer <harald@redhat.com> 013-15
- fixed mdraid container handling
Resolves: rhbz#743240

* Thu Sep 22 2011 Harald Hoyer <harald@redhat.com> 013-13
- fixed mdraid issues
- fixed btrfsck
Resolves: rhbz#735602

* Wed Sep 21 2011 Harald Hoyer <harald@redhat.com> 013-12
- removed patch backup files
- reintroduced /dev/live

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-11
- move mounting of securitfs to a seperate module
Resolves: rhbz#737140

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-10
- mount securitfs with the correct source
Resolves: rhbz#737140

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-9
- do not carry over initramfs udev rules
Resolves: rhbz#734096

* Fri Sep 02 2011 Harald Hoyer <harald@redhat.com> 013-8
- hopefully fixed one part of a loop/udev and loop/mount race
Resolves: rhbz#735199

* Wed Aug 31 2011 Harald Hoyer <harald@redhat.com> 013-7
- add /lib/udev/input_id to the initramfs
- fix hmac install

* Tue Aug 30 2011 Harald Hoyer <harald@redhat.com> 013-6
- fixed environment passing to real init
Resolves: rhbz#733674
- fixed lvm on md

* Mon Aug 29 2011 Harald Hoyer <harald@redhat.com> 013-5
- fixed rhel/fedora version checks

* Wed Aug 17 2011 Harald Hoyer <harald@redhat.com> 013-4
- fixed crash with livenet installed

* Wed Aug 17 2011 Harald Hoyer <harald@redhat.com> 013-3
- fixed live iso mounting
Resolves: rhbz#730579

* Fri Aug 12 2011 Harald Hoyer <harald@redhat.com> 013-1
- fixed symlink creation for lorax

* Wed Aug 10 2011 Harald Hoyer <harald@redhat.com> 011-41.git20110810
- fixed getargs() for empty args

* Wed Aug 10 2011 Harald Hoyer <harald@redhat.com> 011-40.git20110810
- fixed symbolic link creation in the initramfs
Resolves: rhbz#728863

* Wed Jul 20 2011 Harald Hoyer <harald@redhat.com> 011-15.git20110720
- "eject" is optional now
- refined shutdown procedure

* Mon Jul 18 2011 Harald Hoyer <harald@redhat.com> 011-1
- version 011

* Fri May 20 2011 Harald Hoyer <harald@redhat.com> 011-0.1%{?rdist}
- git snapshot of pre-version 011

* Fri Apr 01 2011 Harald Hoyer <harald@redhat.com> 010-1
- version 010

* Thu Mar 31 2011 Harald Hoyer <harald@redhat.com> 009-5
- fixed PATH and kmsg logging

* Thu Mar 31 2011 Harald Hoyer <harald@redhat.com> 009-4
- fixed dmsquash rule generation
- fixed fips boot arg parsing
- fixed plymouth pid generation

* Wed Mar 30 2011 Harald Hoyer <harald@redhat.com> 009-3
- fixed dhcp
- added /lib/firmware/updates to firmware directories 
- fixed LiveCD /dev/.initramfs fallback
- fixed cdrom polling
- dropped net-tools dependency

* Tue Mar 29 2011 Harald Hoyer <harald@redhat.com> 009-2
- fixed empty output file argument handling:
  "dracut '' <kernel version>" 

* Mon Mar 28 2011 Harald Hoyer <harald@redhat.com> 009-1
- version 009

* Thu Mar 17 2011 Harald Hoyer <harald@redhat.com> 009-0.1
- version 009 prerelease

* Tue Feb 22 2011 Harald Hoyer <harald@redhat.com> 008-7
- fixed lvm version parsing

* Tue Feb 22 2011 Harald Hoyer <harald@redhat.com> 008-6
- fixed lvm version parsing

* Mon Feb 21 2011 Harald Hoyer <harald@redhat.com> 008-5
- fixed i18n unicode setting
- set cdrom in kernel polling

* Fri Feb 18 2011 Harald Hoyer <harald@redhat.com> 008-4
- readded dist tag

* Fri Feb 18 2011 Harald Hoyer <harald@redhat.com> 008-3
- fixed i18n
- turned off selinux by default

* Wed Feb 09 2011 Harald Hoyer <harald@redhat.com> 008-2
- do not write dracut.log to /tmp under any circumstances
- touch /dev/.systemd/plymouth after plymouth started

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 008-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Harald Hoyer <harald@redhat.com> 008-1
- version 008-1

* Mon Jan 17 2011 Harald Hoyer <harald@redhat.com> 008-0.11
- removed "mount" requirement

* Thu Nov 18 2010 Harald Hoyer <harald@redhat.com> - 008-0.10
- dracut-008 pre git snapshot
- fixes /dev/dri permissions
Resolves: rhbz#626559

* Fri Nov 12 2010 Harald Hoyer <harald@redhat.com> 008-0.9
- dracut-008 pre git snapshot
- fixes /dev/.udev permissions
Resolves: rhbz#651594

* Wed Nov  3 2010 Harald Hoyer <harald@redhat.com> - 008-0.8
- fixed fsck -a option

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.7
- added fsck to initramfs

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.6
- fixed rpm macros

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.5
- dracut-008 pre git snapshot

* Mon Aug 09 2010 Harald Hoyer <harald@redhat.com> 007-1
- version 007

* Thu Jun 17 2010 Harald Hoyer <harald@redhat.com> 006-1
- version 006

* Fri Jun 11 2010 Harald Hoyer <harald@redhat.com>
- Remove requirements, which are not really needed
Resolves: rhbz#598509
- fixed copy of network config to /dev/.initramfs/ (patch 146)
Resolves: rhbz#594649
- more password beauty (patch 142)
Resolves: rhbz#561092
- support multiple iSCSI disks (patch 143)
Resolves: rbhz#580190
- fixed selinux=0 (patch 130)
Resolves: rhbz#593080
- add support for booting LVM snapshot root volume (patch 145)
Resolves: rbhz#602723
- remove hardware field from BOOTIF= (patch 148)
Resolves: rhbz#599593
- add aes kernel modules and fix crypt handling (patch 137, patch 140 and patch 147)
Resolves: rhbz#600170

* Thu May 27 2010 Harald Hoyer <harald@redhat.com> 
- fixed Requirements
- fixed autoip6 
Resolves: rhbz#538388
- fixed multipath
Resolves: rhbz#595719

* Thu May 06 2010 Harald Hoyer <harald@redhat.com> 
- only display short password messages
Resolves: rhbz#561092

* Thu May 06 2010 Harald Hoyer <harald@redhat.com>
- fixed dracut manpages 
Resolves: rhbz#589109
- use ccw-init and ccw rules from s390utils
Resolves: rhbz#533494
- fixed fcoe
Resolves: rhbz#486244
- various other bugfixes seen in Fedora

* Tue Apr 20 2010 Harald Hoyer <harald@redhat.com> 
- fixed network with multiple nics
- fixed nfsidmap paths
- do not run blkid on non active container raids
- fixed cdrom polling mechanism
- update to latest git

* Thu Apr 15 2010 Harald Hoyer <harald@redhat.com>
- fixed dracut manpages
- dmraid parse different error messages
- add cdrom polling mechanism for slow cdroms
- add module btrfs
- teach dmsquash live-root to use rootflags
- trigger udev with action=add
- fixed add_drivers handling 
- add sr_mod
- use pigz instead of gzip, if available

* Thu Mar 25 2010 Harald Hoyer <harald@redhat.com> 
- removed firmware requirements (rhbz#572634)
- add /etc/dracut.conf.d
- Resolves: rhbz#572634

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 
- version 005

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 
- fixed rpmlint errors (rhbz#570547)
- removed firmware package from dracut-kernel (rhbz#572634)
- add dcb support to dracut's FCoE support (rhbz#563794)
- force install some modules in hostonly mode (rhbz#573094)
- various other bugfixes
- Resolves: rhbz#570547, rhbz#572634, rhbz#563794, rhbz#573094

* Thu Feb 18 2010 Harald Hoyer <harald@redhat.com> 004-15
- fixed "selinux=0" booting (rhbz#566376)
- fixed internal IFS handling
- Resolves: rhbz#566376

* Fri Jan 29 2010 Harald Hoyer <harald@redhat.com> 004-5
- fixed firmware.sh bug (#559975 #559597)

* Tue Jan 26 2010 Harald Hoyer <harald@redhat.com> 004-4
- add multipath check

* Tue Jan 26 2010 Harald Hoyer <harald@redhat.com> 004-3
- fix selinux handling if .autorelabel is present
- Resolves: rhbz#557744

* Wed Jan 20 2010 Harald Hoyer <harald@redhat.com> 004-2
- fix emergency_shell argument parsing
- Related: rhbz#543948

* Fri Jan 15 2010 Harald Hoyer <harald@redhat.com> 004-1
- version 004
- Resolves: rhbz#529339 rhbz#533494 rhbz#548550 
- Resolves: rhbz#548555 rhbz#553195

* Wed Jan 13 2010 Harald Hoyer <harald@redhat.com> 003-3
- add Obsoletes of mkinitrd/nash/libbdevid-python
- Related: rhbz#543948

* Wed Jan 13 2010 Warren Togami <wtogami@redhat.com> 003-2
- nbd is Fedora only

* Fri Nov 27 2009 Harald Hoyer <harald@redhat.com> 003-1
- version 003

* Mon Nov 23 2009 Harald Hoyer <harald@redhat.com> 002-26
- add WITH_SWITCH_ROOT make flag
- add fips requirement conditional
- add more device mapper modules (bug #539656)

* Fri Nov 20 2009 Dennis Gregorovic <dgregor@redhat.com> - 002-25.1
- nss changes for Alpha 3

* Thu Nov 19 2009 Harald Hoyer <harald@redhat.com> 002-25
- add more requirements for dracut-fips (bug #539257)

* Tue Nov 17 2009 Harald Hoyer <harald@redhat.com> 002-24
- put fips module in a subpackage (bug #537619)

* Tue Nov 17 2009 Harald Hoyer <harald@redhat.com> 002-23
- install xdr utils for multipath (bug #463458)

* Thu Nov 12 2009 Harald Hoyer <harald@redhat.com> 002-22
- add module 90multipath
- add module 01fips
- renamed module 95ccw to 95znet (bug #533833)
- crypt: ignore devices in /etc/crypttab (root is not in there)
- dasd: only install /etc/dasd.conf in hostonly mode (bug #533833)
- zfcp: only install /etc/zfcp.conf in hostonly mode (bug #533833)
- kernel-modules: add scsi_dh scsi_dh_rdac scsi_dh_emc (bug #527750)
- dasd: use dasdconf.sh from s390utils (bug #533833)

* Fri Nov 06 2009 Harald Hoyer <harald@redhat.com> 002-21
- fix rd_DASD argument handling (bug #531720)
- Resolves: rhbz#531720

* Wed Nov 04 2009 Harald Hoyer <harald@redhat.com> 002-20
- fix rd_DASD argument handling (bug #531720)
- Resolves: rhbz#531720

* Tue Nov 03 2009 Harald Hoyer <harald@redhat.com> 002-19
- changed rd_DASD to rd_DASD_MOD (bug #531720)
- Resolves: rhbz#531720

* Tue Oct 27 2009 Harald Hoyer <harald@redhat.com> 002-18
- renamed lvm/device-mapper udev rules according to upstream changes
- fixed dracut search path issue

* Mon Oct 26 2009 Harald Hoyer <harald@redhat.com> 002-17
- load dm_mod module (bug #530540)

* Fri Oct 09 2009 Jesse Keating <jkeating@redhat.com> - 002-16
- Upgrade plymouth to Requires(pre) to make it show up before kernel

* Thu Oct 08 2009 Harald Hoyer <harald@redhat.com> 002-15
- s390 ccw: s/layer1/layer2/g

* Thu Oct 08 2009 Harald Hoyer <harald@redhat.com> 002-14
- add multinic support
- add s390 zfcp support
- add s390 network support

* Wed Oct 07 2009 Harald Hoyer <harald@redhat.com> 002-13
- fixed init=<command> handling
- kill loginit if "rdinitdebug" specified
- run dmsquash-live-root after udev has settled (bug #527514)

* Tue Oct 06 2009 Harald Hoyer <harald@redhat.com> 002-12
- add missing loginit helper
- corrected dracut manpage

* Thu Oct 01 2009 Harald Hoyer <harald@redhat.com> 002-11
- fixed dracut-gencmdline for root=UUID or LABEL

* Thu Oct 01 2009 Harald Hoyer <harald@redhat.com> 002-10
- do not destroy assembled raid arrays if mdadm.conf present
- mount /dev/shm 
- let udevd not resolve group and user names
- preserve timestamps of tools on initramfs generation
- generate symlinks for binaries correctly
- moved network from udev to initqueue
- mount nfs3 with nfsvers=3 option and retry with nfsvers=2
- fixed nbd initqueue-finished
- improved debug output: specifying "rdinitdebug" now logs
  to dmesg, console and /init.log
- stop udev before killing it
- add ghost /var/log/dracut.log
- dmsquash: use info() and die() rather than echo
- strip kernel modules which have no x bit set
- redirect stdin, stdout, stderr all RW to /dev/console
  so the user can use "less" to view /init.log and dmesg

* Tue Sep 29 2009 Harald Hoyer <harald@redhat.com> 002-9
- make install of new dm/lvm udev rules optionally
- correct dasd module typo

* Fri Sep 25 2009 Warren Togami <wtogami@redhat.com> 002-8
- revert back to dracut-002-5 tarball 845dd502
  lvm2 was reverted to pre-udev

* Wed Sep 23 2009 Harald Hoyer <harald@redhat.com> 002-7
- build with the correct tarball

* Wed Sep 23 2009 Harald Hoyer <harald@redhat.com> 002-6
- add new device mapper udev rules and dmeventd 
  bug 525319, 525015

* Wed Sep 23 2009 Warren Togami <wtogami@redaht.com> 002-5
- Revert back to -3, Add umount back to initrd
  This makes no functional difference to LiveCD.  See Bug #525319

* Mon Sep 21 2009 Warren Togami <wtogami@redhat.com> 002-4
- Fix LiveCD boot regression

* Mon Sep 21 2009 Harald Hoyer <harald@redhat.com> 002-3
- bail out if selinux policy could not be loaded and 
  selinux=0 not specified on kernel command line 
  (bug #524113)
- set finished criteria for dmsquash live images

* Fri Sep 18 2009 Harald Hoyer <harald@redhat.com> 002-2
- do not cleanup dmraids
- copy over lvm.conf

* Thu Sep 17 2009 Harald Hoyer <harald@redhat.com> 002-1
- version 002
- set correct PATH
- workaround for broken mdmon implementation

* Wed Sep 16 2009 Harald Hoyer <harald@redhat.com> 001-12
- removed lvm/mdraid/dmraid lock files
- add missing ifname= files

* Wed Sep 16 2009 Harald Hoyer <harald@redhat.com> 001-11
- generate dracut-version during rpm build time

* Tue Sep 15 2009 Harald Hoyer <harald@redhat.com> 001-10
- add ifname= argument for persistent netdev names
- new /initqueue-finished to check if the main loop can be left
- copy mdadm.conf if --mdadmconf set or mdadmconf in dracut.conf

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-9
- added Requires: plymouth-scripts

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-8
- plymouth: use plymouth-populate-initrd
- add add_drivers for dracut and dracut.conf
- do not mount /proc and /selinux manually in selinux-load-policy

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-7
- add scsi_wait_scan to be sure everything was scanned

* Tue Sep 08 2009 Harald Hoyer <harald@redhat.com> 001-6
- fixed several problems with md raid containers
- fixed selinux policy loading

* Tue Sep 08 2009 Harald Hoyer <harald@redhat.com> 001-5
- patch does not honor file modes, fixed them manually

* Mon Sep 07 2009 Harald Hoyer <harald@redhat.com> 001-4
- fixed mdraid for IMSM

* Mon Sep 07 2009 Harald Hoyer <harald@redhat.com> 001-3
- fixed bug, which prevents installing 61-persistent-storage.rules (bug #520109)

* Thu Sep 03 2009 Harald Hoyer <harald@redhat.com> 001-2
- fixed missing grep for md
- reorder cleanup

* Wed Sep 02 2009 Harald Hoyer <harald@redhat.com> 001-1
- version 001
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Aug 14 2009 Harald Hoyer <harald@redhat.com> 0.9-1
- version 0.9

* Thu Aug 06 2009 Harald Hoyer <harald@redhat.com> 0.8-1
- version 0.8 
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Jul 24 2009 Harald Hoyer <harald@redhat.com> 0.7-1
- version 0.7
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Wed Jul 22 2009 Harald Hoyer <harald@redhat.com> 0.6-1
- version 0.6
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Jul 17 2009 Harald Hoyer <harald@redhat.com> 0.5-1
- version 0.5
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Sat Jul 04 2009 Harald Hoyer <harald@redhat.com> 0.4-1
- version 0.4
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Thu Jul 02 2009 Harald Hoyer <harald@redhat.com> 0.3-1
- version 0.3
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Wed Jul 01 2009 Harald Hoyer <harald@redhat.com> 0.2-1
- version 0.2

* Fri Jun 19 2009 Harald Hoyer <harald@redhat.com> 0.1-1
- first release

* Thu Dec 18 2008 Jeremy Katz <katzj@redhat.com> - 0.0-1
- Initial build
