Name     : jdk-xmlunit
Version  : 1.6
Release  : 3
URL      : http://downloads.sourceforge.net/xmlunit/xmlunit-1.6-src.zip
Source0  : http://downloads.sourceforge.net/xmlunit/xmlunit-1.6-src.zip
Source1  : http://repo1.maven.org/maven2/xmlunit/xmlunit/1.6/xmlunit-1.6.pom
Summary  : No detailed summary available
Group    : Development/Tools
License  : BSD-3-Clause
BuildRequires : apache-ant
BuildRequires : javapackages-tools
BuildRequires : jdk-junit4
BuildRequires : lxml
BuildRequires : openjdk-dev
BuildRequires : python3
BuildRequires : six

%description
XMLUnit extends JUnit to simplify unit testing of XML. It compares a control XML document to a test document or the result of a transformation, validates documents against a DTD, and (from v0.5) compares the results of XPath expressions.

%prep
%setup -q -n xmlunit-1.6

sed -i /java.class.path/d build.xml
# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc

cat >build.properties <<EOF
junit.lib=$(build-classpath junit)
xmlxsl.lib=
test.report.dir=test
EOF

cat >docbook.properties <<EOF
db5.xsl=/usr/share/sgml/docbook/xsl-ns-stylesheets
EOF

%build
ant -Dbuild.compiler=modern -Dhaltonfailure=yes jar javadocs

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/maven-poms
mkdir -p %{buildroot}/usr/share/maven-metadata
mkdir -p %{buildroot}/usr/share/java

cp build/lib/xmlunit-1.6.jar %{buildroot}/usr/share/java/xmlunit.jar
cp %{SOURCE1} %{buildroot}/usr/share/maven-poms/xmlunit.pom

# Creates metadata
python3 /usr/share/java-utils/maven_depmap.py \
-n "" \
--pom-base %{buildroot}/usr/share/maven-poms \
--jar-base %{buildroot}/usr/share/java \
%{buildroot}/usr/share/maven-metadata/xmlunit.xml \
%{buildroot}/usr/share/maven-poms/xmlunit.pom \
%{buildroot}/usr/share/java/xmlunit.jar \

%files
%defattr(-,root,root,-)
/usr/share/java/xmlunit.jar
/usr/share/maven-metadata/xmlunit.xml
/usr/share/maven-poms/xmlunit.pom
