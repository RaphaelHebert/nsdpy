mocked_response_xms = ('''<DocSum>
        <Id>1691430259</Id>
        <Item Name="Caption" Type="String">MH518723</Item>
        <Item Name="Title" Type="String">Parnassius nomion isolate BMS03 cytochrome c oxidase subunit I (COI) gene, partial cds; mitochondrial</Item>
        <Item Name="Extra" Type="String">gi|1691430259|gb|MH518723.1|[1691430259]</Item>
        <Item Name="Gi" Type="Integer">1691430259</Item>
        <Item Name="CreateDate" Type="String">2019/12/30</Item>
        <Item Name="UpdateDate" Type="String">2019/12/30</Item>
        <Item Name="Flags" Type="Integer">0</Item>
        <Item Name="TaxId" Type="Integer">213955</Item>
        <Item Name="Length" Type="Integer">648</Item>
        <Item Name="Status" Type="String">live</Item>
        <Item Name="ReplacedBy" Type="String"></Item>
        <Item Name="Comment" Type="String"><![CDATA[  ]]></Item>
        <Item Name="AccessionVersion" Type="String">MH518723.1</Item>
</DocSum>

<DocSum>
        <Id>1691430257</Id>
        <Item Name="Caption" Type="String">MH518722</Item>
        <Item Name="Title" Type="String">Parnassius nomion isolate BMS02 cytochrome c oxidase subunit I (COI) gene, partial cds; mitochondrial</Item>
        <Item Name="Extra" Type="String">gi|1691430257|gb|MH518722.1|[1691430257]</Item>
        <Item Name="Gi" Type="Integer">1691430257</Item>
        <Item Name="CreateDate" Type="String">2019/12/30</Item>
        <Item Name="UpdateDate" Type="String">2019/12/30</Item>
        <Item Name="Flags" Type="Integer">0</Item>
        <Item Name="TaxId" Type="Integer">213955</Item>
        <Item Name="Length" Type="Integer">648</Item>
        <Item Name="Status" Type="String">live</Item>
        <Item Name="ReplacedBy" Type="String"></Item>
        <Item Name="Comment" Type="String"><![CDATA[  ]]></Item>
        <Item Name="AccessionVersion" Type="String">MH518722.1</Item>
</DocSum>

<DocSum>
        <Id>1691430255</Id>
        <Item Name="Caption" Type="String">MH518721</Item>
        <Item Name="Title" Type="String">Parnassius nomion isolate BMS01 cytochrome c oxidase subunit I (COI) gene, partial cds; mitochondrial</Item>
        <Item Name="Extra" Type="String">gi|1691430255|gb|MH518721.1|[1691430255]</Item>
        <Item Name="Gi" Type="Integer">1691430255</Item>
        <Item Name="CreateDate" Type="String">2019/12/30</Item>
        <Item Name="UpdateDate" Type="String">2019/12/30</Item>
        <Item Name="Flags" Type="Integer">0</Item>
        <Item Name="TaxId" Type="Integer">213955</Item>
        <Item Name="Length" Type="Integer">648</Item>
        <Item Name="Status" Type="String">live</Item>
        <Item Name="ReplacedBy" Type="String"></Item>
        <Item Name="Comment" Type="String"><![CDATA[  ]]></Item>
        <Item Name="AccessionVersion" Type="String">MH518721.1</Item>
</DocSum>

</eSummaryResult>''')


expected_output = {"MH518723.1": "213955", "MH518722.1": "213955", "MH518721.1": "213955"}