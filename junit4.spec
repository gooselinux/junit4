# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           junit4
Version:        4.5
Release:        5.3%{?dist}
Epoch:          0
Summary:        Java regression test package
License:        CPL
URL:            http://www.junit.org/
Group:          Development/Tools
# cvs -d:pserver:anonymous@junit.cvs.sourceforge.net:/cvsroot/junit login
# cvs -z3 -d:pserver:anonymous@junit.cvs.sourceforge.net:/cvsroot/junit export -r r45 -d junit-4.5 junit
# tar cjf junit-4.5.tar.bz2 junit-4.5/
Source0:        junit-4.5.tar.bz2
Source1:        junit-4.5.pom
Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4
Requires:       hamcrest
Requires:       java-1.6.0
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-1.6.0-devel
BuildRequires:  hamcrest
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:          Documentation
Summary:        Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Libraries
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n junit-%{version}
find . -type f -name "*.jar" | xargs -t rm
ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.1.jar
perl -pi -e 's/\r$//g' stylesheet.css

%build
export CLASSPATH=
export OPT_JAR_LIST=:
ant -Dant.build.javac.source=1.5 dist

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 junit%{version}/junit-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir} 
ln -sf %{name}-%{version}.jar %{name}.jar
popd

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap junit junit %{version} JPP %{name}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr junit%{version}/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/demo/junit # Not using %name for last part because it is 
                                                                # part of package name
cp -pr junit%{version}/junit/* $RPM_BUILD_ROOT%{_datadir}/%{name}/demo/junit

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc cpl-v10.html README.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc junit%{version}/doc/*

%changelog
* Thu Jan 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:4.5-5.3
- Drop gcj_support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:4.5-5.2
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.5-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.5-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:4.5-3.1
- build for Fedora

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:4.5-3
- reorder %%files list

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:4.5-2
- fix GCJ support
- fix javadoc symlink

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:4.5-1
- 4.5

* Thu Mar 06 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.4-1jpp
- 4.4
- Switch to CVS for sources

* Mon Feb 11 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-4jpp
- Fix versioned jar name, was junit-4.3.1
- Restore Epoch

* Fri Jan 25 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-3jpp
- build and upload noarch packages
- Add pom and depmap frag
- BR java-devel = 1.5.0
- Restore Vendor, Distribution from macros

* Tue Aug 07 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-2jpp
- Set gcj_support to 0 to work around problems with GCJ.
- Fix buglet with the gcj post/postun if statement.
- Fix tab / space problems.
- Fix buildroot.
- Update Summary.
- Convert html files to Unix file endings.
- Disable aot-compile-rpm because it's not working ATM.

* Mon Jul 09 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-1jpp
- 4.3.1.

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Sun Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Sat Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Mon Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp 
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp 
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
